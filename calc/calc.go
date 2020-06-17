package calc

import (
	"fmt"
	"runtime"

	"github.com/timdrysdale/gorad/core"
	"github.com/timdrysdale/pool"
)

//"github.com/timdrysdale/pool"

func DoCalcs(calcs []*core.Calc) []error {

	tasks := []*pool.Task{}

	for _, c := range calcs {

		newtask := pool.NewTask(func() error {
			return Calc(c)
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

func Calc(calc *core.Calc) error {

	fmt.Println(calc)
	return nil
}
