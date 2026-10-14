// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
package common

import (
	"context"
	"errors"
	"sync/atomic"
	"testing"
	"time"
)

func TestDependencyReadyWithoutStageBarrier(t *testing.T) {
	ctx, cancel := context.WithTimeout(context.Background(), 3*time.Second)
	defer cancel()
	gate := NewJobAdmission(ctx, 2)
	defer gate.Close()
	longStarted := make(chan struct{})
	dependentRan := make(chan struct{})
	var prerequisiteDone atomic.Bool
	jobs := []DependencyJob{
		{ID: "long", Run: gate.Wrap(func(ctx context.Context) error {
			close(longStarted)
			select {
			case <-dependentRan:
				return nil
			case <-ctx.Done():
				return ctx.Err()
			}
		})},
		{ID: "prerequisite", Run: gate.Wrap(func(ctx context.Context) error {
			select {
			case <-longStarted:
				prerequisiteDone.Store(true)
				return nil
			case <-ctx.Done():
				return ctx.Err()
			}
		})},
		{ID: "dependent", Needs: []string{"prerequisite"}, Run: gate.Wrap(func(context.Context) error {
			if !prerequisiteDone.Load() {
				t.Error("dependent started before its prerequisite")
			}
			close(dependentRan)
			return nil
		})},
	}
	if err := NewDependencyExecutor(jobs)(ctx); err != nil {
		t.Fatal(err)
	}
}

func TestDependencyFailureAndInvalidGraphs(t *testing.T) {
	failure := errors.New("planted predecessor failure")
	var called atomic.Bool
	jobs := []DependencyJob{
		{ID: "first", Run: func(context.Context) error { return failure }},
		{ID: "next", Needs: []string{"first"}, Run: func(context.Context) error { called.Store(true); return nil }},
	}
	if err := NewDependencyExecutor(jobs)(context.Background()); !errors.Is(err, failure) || called.Load() {
		t.Fatalf("err=%v dependent=%v", err, called.Load())
	}
	for _, needs := range [][]string{{"missing"}, {"next"}} {
		jobs[1].Needs = needs
		if err := NewDependencyExecutor(jobs)(context.Background()); err == nil {
			t.Fatal("invalid graph accepted")
		}
	}
	if err := NewDependencyExecutor([]DependencyJob{jobs[0], jobs[0]})(context.Background()); err == nil {
		t.Fatal("duplicate job accepted")
	}
	ctx, cancel := context.WithCancel(context.Background())
	cancel()
	jobs[1].Needs = nil
	if err := NewDependencyExecutor(jobs[1:])(ctx); !errors.Is(err, context.Canceled) || called.Load() {
		t.Fatalf("cancelled parent: %v started=%v", err, called.Load())
	}
}
