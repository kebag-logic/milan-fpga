// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
package common

import (
	"context"
	"fmt"
	"sync"
)

// DependencyJob waits only for its declared prerequisites, never a plan stage.
// Its executor owns matrix concurrency; physical legs use the shared admission gate.
type DependencyJob struct {
	ID    string
	Needs []string
	Run   Executor
}

// NewDependencyExecutor joins every started job and preserves the first failure.
func NewDependencyExecutor(jobs []DependencyJob) Executor {
	return func(parent context.Context) error {
		ctx, cancel := context.WithCancel(parent)
		defer cancel()
		byID := map[string]DependencyJob{}
		done := map[string]chan struct{}{}
		for _, job := range jobs {
			if _, exists := byID[job.ID]; exists || job.Run == nil {
				return fmt.Errorf("duplicate or invalid dependency job %q", job.ID)
			}
			byID[job.ID] = job
			done[job.ID] = make(chan struct{})
		}
		state := map[string]int{}
		var visit func(string) error
		visit = func(id string) error {
			job, exists := byID[id]
			if !exists {
				return fmt.Errorf("missing dependency %q", id)
			}
			if state[id] == 1 {
				return fmt.Errorf("cyclic dependency %q", id)
			}
			if state[id] == 2 {
				return nil
			}
			state[id] = 1
			for _, need := range job.Needs {
				if err := visit(need); err != nil {
					return err
				}
			}
			state[id] = 2
			return nil
		}
		for _, job := range jobs {
			if err := visit(job.ID); err != nil {
				return err
			}
		}
		var workers sync.WaitGroup
		var lock sync.Mutex
		var firstErr error
		for _, job := range jobs {
			workers.Add(1)
			go func() {
				defer workers.Done()
				for _, need := range job.Needs {
					select {
					case <-ctx.Done():
						return
					case <-done[need]:
					}
				}
				if ctx.Err() != nil {
					return
				}
				if err := job.Run(ctx); err != nil {
					lock.Lock()
					if firstErr == nil {
						firstErr = err
						cancel()
					}
					lock.Unlock()
				}
				close(done[job.ID])
			}()
		}
		workers.Wait()
		if firstErr != nil {
			return firstErr
		}
		return parent.Err()
	}
}
