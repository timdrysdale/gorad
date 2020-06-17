package lvfile

import (
	"testing"

	mgl "github.com/go-gl/mathgl/mgl64"
	"github.com/stretchr/testify/assert"
)

func TestParseDATFile(t *testing.T) {

	samples, err := ParseDATFile("test/test.dat")

	assert.NoError(t, err)

	assert.Equal(t, 5, len(samples))
	assert.Equal(t, mgl.Vec3{-65, -65, 0}, samples[0].Pos)
	assert.Equal(t, mgl.Vec3{-65, -65, 0}, samples[1].Pos)

	assert.Equal(t, 9.000000E+9, samples[0].Freq)
	assert.Equal(t, 9.015000E+9, samples[4].Freq)
	assert.Equal(t, complex(3.499985E-4, 1.780128E-2), samples[0].Val)
	assert.Equal(t, complex(1.414394E-2, 1.187611E-2), samples[3].Val)

}
