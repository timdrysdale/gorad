package core

import (
	"fmt"

	mgl "github.com/go-gl/mathgl/mgl64"
)

func CreateField(farfield Farfield) ([]Sample, error) {

	samples := []Sample{}

	if farfield.Points < 2 {
		return samples, fmt.Errorf("Need at least two points per axis to make a plane, got %d", farfield.Points)
	}

	switch farfield.Plane {
	case "XY":
	case "XZ":
	case "YZ":
	default:
		return samples, fmt.Errorf("Unknown plane type %s", farfield.Plane)
	}

	dx := farfield.Width / (float64(farfield.Points - 1))

	left := -farfield.Width / 2.

	line := []float64{left}

	for i := 1; i < farfield.Points; i++ {

		point := left + dx*float64(i)
		line = append(line, point)
	}

	for _, x := range line {
		for _, y := range line {

			newSample := Sample{}

			switch farfield.Plane {

			case "XY":
				newSample = Sample{
					Pos:  mgl.Vec3{x, y, farfield.Intersect},
					Freq: farfield.Freq,
				}
			case "XZ":

				newSample = Sample{
					Pos:  mgl.Vec3{x, farfield.Intersect, y},
					Freq: farfield.Freq,
				}

			case "YZ":
				newSample = Sample{
					Pos:  mgl.Vec3{farfield.Intersect, x, y},
					Freq: farfield.Freq,
				}
			}

			samples = append(samples, newSample)

		}
	}

	return samples, nil

}
