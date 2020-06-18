package calc

import (
	"fmt"
	"math"
	"math/cmplx"
	"runtime"

	"github.com/timdrysdale/gorad/core"
	"github.com/timdrysdale/pool"
)

//"github.com/timdrysdale/pool"

func DoCalcs(calcs []*core.Calc) []error {

	tasks := []*pool.Task{}

	for _, c := range calcs {

		thisCalc := c
		newtask := pool.NewTask(func() error {
			return DoCalc(thisCalc)
		})

		tasks = append(tasks, newtask)

	}

	p := pool.NewPool(tasks, runtime.GOMAXPROCS(-1))

	p.Run()

	errorList := []error{}

	for _, task := range p.Tasks {
		if task.Err != nil {
			errorList = append(errorList, task.Err)
		}
	}

	return errorList

}

func DoCalc(calc *core.Calc) error {

	fmt.Printf("Doing %v\n", calc.Setup)

	ffSamples, err := core.CreateField(calc.Setup)

	if err != nil {
		return err
	}

	calc.Farfields = &ffSamples

	for idx, ff := range *calc.Farfields {

		for _, src := range *calc.Sources {
			propagateField(&src, &ff)
		}

		(*calc.Farfields)[idx] = ff
	}
	return nil

}

func propagateField(source, destination *core.Sample) {

	r := destination.Pos.Sub(source.Pos).Len()
	k := wavevector(float64(source.Freq / 1000)) //scale the frequency by mm/m

	contribution := source.Val * cmplx.Exp(complex(0, k*r)) / complex(4*math.Pi*r, 0)

	destination.Val = destination.Val + contribution
}

func wavevector(frequency float64) float64 {

	return 2 * math.Pi * frequency / 299792458
}
