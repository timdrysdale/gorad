package grfile

import (
	"testing"

	mgl "github.com/go-gl/mathgl/mgl64"
	"github.com/stretchr/testify/assert"
	"github.com/timdrysdale/gorad/core"
)

func TestConvertSamplesToFileSamples(t *testing.T) {

	input := []core.Sample{
		core.Sample{
			Pos: mgl.Vec3{1, 2, 3},
			Val: complex(10, 20),
		},
		core.Sample{
			Pos: mgl.Vec3{4, 5, 6},
			Val: complex(30, 40),
		},
	}

	fileSamples := ConvertSamplesToFileSamples(input)

	assert.Equal(t, 2, len(fileSamples))
	assert.Equal(t, 1., fileSamples[0].X)
	assert.Equal(t, 2., fileSamples[0].Y)
	assert.Equal(t, 3., fileSamples[0].Z)
	assert.Equal(t, 10., fileSamples[0].Real)
	assert.Equal(t, 20., fileSamples[0].Imag)
	assert.Equal(t, 4., fileSamples[1].X)
	assert.Equal(t, 5., fileSamples[1].Y)
	assert.Equal(t, 6., fileSamples[1].Z)
	assert.Equal(t, 30., fileSamples[1].Real)
	assert.Equal(t, 40., fileSamples[1].Imag)

}
