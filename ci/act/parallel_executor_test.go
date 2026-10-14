// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
package common

import (
	"context"
	"errors"
	"sync"
	"sync/atomic"
	"testing"
)

func TestBoundedFailureStopsAdmission(t *testing.T) {
	var started atomic.Int32
	var cleaned atomic.Int32
	var ready sync.WaitGroup
	ready.Add(4)
	failure := errors.New("planted job failure")
	executors := make([]Executor, 40)
	for i := range executors {
		executors[i] = func(ctx context.Context) error {
			index := started.Add(1)
			defer cleaned.Add(1)
			if index > 4 {
				t.Error("a queued job was admitted after failure")
				return nil
			}
			ready.Done()
			ready.Wait()
			if index == 1 {
				return failure
			}
			<-ctx.Done()
			return ctx.Err()
		}
	}
	if err := NewFailFastParallelExecutor(4, executors...)(context.Background()); !errors.Is(err, failure) {
		t.Fatalf("lost first failure: %v", err)
	}
	if started.Load() != 4 || cleaned.Load() != 4 {
		t.Fatalf("started=%d cleaned=%d", started.Load(), cleaned.Load())
	}
}

func TestBoundedSuccessRunsEveryJob(t *testing.T) {
	var started atomic.Int32
	var running atomic.Int32
	var peak atomic.Int32
	var ready sync.WaitGroup
	ready.Add(4)
	executors := make([]Executor, 40)
	for i := range executors {
		executors[i] = func(_ context.Context) error {
			active := running.Add(1)
			defer running.Add(-1)
			for old := peak.Load(); active > old && !peak.CompareAndSwap(old, active); old = peak.Load() {
			}
			if started.Add(1) <= 4 {
				ready.Done()
				ready.Wait()
			}
			return nil
		}
	}
	if err := NewFailFastParallelExecutor(4, executors...)(context.Background()); err != nil {
		t.Fatal(err)
	}
	if started.Load() != 40 || running.Load() != 0 || peak.Load() != 4 {
		t.Fatalf("started=%d running=%d peak=%d", started.Load(), running.Load(), peak.Load())
	}
}

func TestCancelledParentStartsNoJobs(t *testing.T) {
	ctx, cancel := context.WithCancel(context.Background())
	cancel()
	called := false
	err := NewFailFastParallelExecutor(4, func(context.Context) error { called = true; return nil })(ctx)
	if !errors.Is(err, context.Canceled) || called {
		t.Fatalf("err=%v called=%t", err, called)
	}
}
