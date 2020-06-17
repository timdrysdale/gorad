package core

import (
	mgl "github.com/go-gl/mathgl/mgl64"
)

type Sample struct {
	Pos  mgl.Vec3
	Freq int
	Val  complex128
}

type FileSample struct {
	Freq       int
	X, Y, Z    float64
	Real, Imag float64
}
