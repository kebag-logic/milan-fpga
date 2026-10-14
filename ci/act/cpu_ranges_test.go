// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
package common

import (
	"context"
	"fmt"
	"strings"
	"sync"
	"testing"
	"time"
)

func TestCPURangeRefusals(t *testing.T) {
	for _, raw := range []string{"", "0-7", "1-16", "0-15,12-23", "0-15,0-15", "-1-14", "00-15", "16-0", "0-15,"} {
		if _, err := ParseCPURanges(raw, 12); err == nil {
			t.Fatalf("accepted %q", raw)
		}
	}
	for _, raw := range []string{"0-15,16-31,32-47,48-63", "0-11,12-23,24-35,36-47", "0-15,24-35"} {
		if _, err := ParseCPURanges(raw, 12); err != nil {
			t.Fatal(err)
		}
	}
	if _, err := NewCPUJobAdmission(context.Background(), 4, "0-15", "12"); err == nil {
		t.Fatal("too few ranges accepted")
	}
	if _, _, err := JobCPUOptions(context.Background(), ""); err == nil {
		t.Fatal("unpinned creation accepted")
	}
}

func TestCPUCreationAndNonoverlap(t *testing.T) {
	gate, err := NewCPUJobAdmission(context.Background(), 4, "0-15,16-31,32-47,48-63", "12")
	if err != nil {
		t.Fatal(err)
	}
	defer gate.Close()
	var lock sync.Mutex
	held := map[string]bool{}
	var started, peak int
	work := []Executor{}
	for i := 0; i < 20; i++ {
		work = append(work, gate.Wrap(func(ctx context.Context) error {
			options, cpus, err := JobCPUOptions(ctx, "--memory=8g")
			if err != nil {
				return err
			}
			if !strings.HasSuffix(options, " --cpuset-cpus="+cpus) {
				return fmt.Errorf("create lacks range")
			}
			if _, _, err := JobCPUOptions(ctx, "--cpuset-cpus=0-15"); err == nil {
				return fmt.Errorf("override accepted")
			}
			lock.Lock()
			if held[cpus] {
				lock.Unlock()
				return fmt.Errorf("two jobs share %s", cpus)
			}
			held[cpus] = true
			started++
			if len(held) > peak {
				peak = len(held)
			}
			lock.Unlock()
			time.Sleep(time.Millisecond)
			_, later, err := JobCPUOptions(ctx, "--memory=8g")
			if err != nil || later != cpus {
				return fmt.Errorf("job moved")
			}
			lock.Lock()
			delete(held, cpus)
			lock.Unlock()
			return nil
		}))
	}
	if err := NewFailFastParallelExecutor(20, work...)(context.Background()); err != nil {
		t.Fatal(err)
	}
	if started != 20 || peak != 4 || len(held) != 0 {
		t.Fatalf("started %d peak %d held %v", started, peak, held)
	}
}

func TestCPUFailedCleanupStopsReuse(t *testing.T) {
	gate, err := NewCPUJobAdmission(context.Background(), 1, "0-11", "12")
	if err != nil {
		t.Fatal(err)
	}
	defer gate.Close()
	failure := fmt.Errorf("container removal failed")
	if err := gate.Wrap(func(context.Context) error { return failure })(context.Background()); err != failure {
		t.Fatal(err)
	}
	ran := false
	err = gate.Wrap(func(context.Context) error { ran = true; return nil })(context.Background())
	if ran || err != failure {
		t.Fatalf("failed cleanup reused range: %v %v", ran, err)
	}
}
