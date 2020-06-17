package core

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestCreateField(t *testing.T) {

	samples, err := CreateField(Farfield{
		Freq:      10,
		Plane:     "XY",
		Intersect: 5000,
		Width:     1000,
		Points:    3,
	})

	assert.NoError(t, err)

	assert.Equal(t, 9, len(samples))

	assert.Equal(t, 5000., samples[0].Pos.Z())

	dimMap := make(map[int]map[int]bool)

	for _, sample := range samples {

		x := int(sample.Pos.X())

		y := int(sample.Pos.Y())

		if _, ok := dimMap[x]; !ok {
			dimMap[x] = make(map[int]bool)
		}

		xm := dimMap[x]

		xm[y] = true

		dimMap[x] = xm

	}

	xm1 := map[int]bool{
		-500: true,
		0:    true,
		500:  true,
	}
	assert.Equal(t, xm1, dimMap[-500])

}
