// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
package common

import (
	"context"
	"sync"
)

// RecordedJobExecutor exposes failed steps after the job's cleanup has finished.
// The upstream job executor records step failures in its context and returns nil.
func RecordedJobExecutor(executor Executor) Executor {
	return func(ctx context.Context) error {
		jobContext := WithJobErrorContainer(ctx)
		if err := executor(jobContext); err != nil {
			return err
		}
		return JobError(jobContext)
	}
}

// JobAdmission shares one physical-container limit across nested job matrices.
type JobAdmission struct {
	ctx     context.Context
	cancel  context.CancelFunc
	slots   chan string
	lock    sync.Mutex
	failure error
}

func NewJobAdmission(ctx context.Context, limit int) *JobAdmission {
	if limit < 1 {
		limit = 1
	}
	child, cancel := context.WithCancel(ctx)
	gate := &JobAdmission{ctx: child, cancel: cancel, slots: make(chan string, limit)}
	for i := 0; i < limit; i++ {
		gate.slots <- ""
	}
	return gate
}

func (gate *JobAdmission) Close() { gate.cancel() }

func (gate *JobAdmission) stopped() error {
	if gate.failure != nil {
		return gate.failure
	}
	return gate.ctx.Err()
}

// Wrap reserves a container slot only for an actual matrix leg, never its group.
func (gate *JobAdmission) Wrap(executor Executor) Executor {
	return func(context.Context) error {
		var cpus string
		select {
		case <-gate.ctx.Done():
			gate.lock.Lock()
			defer gate.lock.Unlock()
			return gate.stopped()
		case cpus = <-gate.slots:
		}
		defer func() { gate.slots <- cpus }()
		gate.lock.Lock()
		if err := gate.stopped(); err != nil {
			gate.lock.Unlock()
			return err
		}
		gate.lock.Unlock()
		err := executor(context.WithValue(gate.ctx, jobCPUKey{}, cpus))
		gate.lock.Lock()
		defer gate.lock.Unlock()
		if err != nil && gate.failure == nil {
			gate.failure = err
			gate.cancel()
		}
		if gate.failure != nil {
			return gate.failure
		}
		return err
	}
}
