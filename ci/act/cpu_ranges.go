// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
package common

import (
	"context"
	"fmt"
	"strconv"
	"strings"
)

type jobCPUKey struct{}

// ParseCPURanges accepts only explicitly booked, aligned, disjoint ranges.
// The fallback width comes from the runner's one named setting.
func ParseCPURanges(raw string, fallback int) ([]string, error) {
	if raw == "" {
		return nil, fmt.Errorf("missing CPU ranges")
	}
	if fallback < 1 || fallback > 16 {
		return nil, fmt.Errorf("invalid fallback CPU width")
	}
	ranges := strings.Split(raw, ",")
	held := map[int]bool{}
	for _, span := range ranges {
		ends := strings.Split(span, "-")
		if len(ends) != 2 {
			return nil, fmt.Errorf("invalid CPU range %q", span)
		}
		first, err1 := strconv.Atoi(ends[0])
		last, err2 := strconv.Atoi(ends[1])
		width := last - first + 1
		if err1 != nil || err2 != nil || first < 0 || last < first ||
			fmt.Sprintf("%d-%d", first, last) != span {
			return nil, fmt.Errorf("invalid CPU range %q", span)
		}
		if width != 16 && width != fallback {
			return nil, fmt.Errorf("CPU range %q has unsupported width", span)
		}
		if first%width != 0 {
			return nil, fmt.Errorf("CPU range %q is not aligned", span)
		}
		for cpu := first; cpu <= last; cpu++ {
			if held[cpu] {
				return nil, fmt.Errorf("CPU ranges share CPU %d", cpu)
			}
			held[cpu] = true
		}
	}
	return ranges, nil
}

// NewCPUJobAdmission reserves a range before entering any job executor.
// Failed cleanup stops admission before a range can be reused.
func NewCPUJobAdmission(ctx context.Context, limit int, raw, fallbackText string) (*JobAdmission, error) {
	fallback, err := strconv.Atoi(fallbackText)
	if err != nil {
		return nil, fmt.Errorf("missing fallback CPU width")
	}
	ranges, err := ParseCPURanges(raw, fallback)
	if err != nil {
		return nil, err
	}
	if limit < 1 || len(ranges) < limit {
		return nil, fmt.Errorf("insufficient CPU ranges for %d jobs", limit)
	}
	gate := NewJobAdmission(ctx, limit)
	for i := 0; i < limit; i++ {
		<-gate.slots
		gate.slots <- ranges[i]
	}
	return gate, nil
}

// JobCPUOptions binds the initial Docker create to the admitted range.
// No later container update is required or allowed by this scheduler.
func JobCPUOptions(ctx context.Context, options string) (string, string, error) {
	cpus, _ := ctx.Value(jobCPUKey{}).(string)
	if cpus == "" {
		return "", "", fmt.Errorf("job has no reserved CPU range")
	}
	if strings.Contains(options, "cpuset") || strings.Contains(options, "--cpus") {
		return "", "", fmt.Errorf("job options override reserved CPU range")
	}
	return options + " --cpuset-cpus=" + cpus, cpus, nil
}
