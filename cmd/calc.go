/*
Copyright © 2020 Tim Drysdale <timothy.d.drysdale@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
*/
package cmd

import (
	"fmt"
	"os"
	"path/filepath"

	"github.com/spf13/cobra"
	"github.com/timdrysdale/gorad/calc"
	"github.com/timdrysdale/gorad/core"
	"github.com/timdrysdale/gorad/grfile"
	"github.com/timdrysdale/gorad/util"
)

// calcCmd represents the calc command
var calcCmd = &cobra.Command{
	Use:   "calc [farfields-file] [sources-dir] [output-dir]",
	Short: "Calculate farfields for the source files",
	Args:  cobra.ExactArgs(3),
	Long:  `Each line in the farfields-file defines a frequency for which there must be a corresponding file in sources-dir, and causes the calculation of the specified farfield on a plane at frequency, putting the results in a file in output-dir`,
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("calc called")
		farfieldsFile := os.Args[2]
		sourceDir := os.Args[3]
		outputDir := os.Args[4]

		farfields, err := grfile.ReadFarfields(farfieldsFile)
		if err != nil {
			fmt.Println(err)
			os.Exit(1)
		}

		calcs := []*core.Calc{}

		for _, ff := range farfields {

			sourcePath := filepath.Join(sourceDir, fmt.Sprintf("%d-freq.csv", ff.Freq))

			sources, err := grfile.ReadFreq(sourcePath)

			if err != nil {
				fmt.Println(err)
				os.Exit(1)
			}

			calcs = append(calcs, &core.Calc{
				Sources: &sources,
				Setup:   *ff,
			})
		}
		//[]*core.Farfield, error)
		//	calcs []*core.Calc
		errList := calc.DoCalcs(calcs)
		if len(errList) > 0 {
			fmt.Println(errList)
		}

		util.EnsureDirAll(outputDir)

		for _, calc := range calcs {

			err := grfile.SaveResults(calc, outputDir)
			if err != nil {
				fmt.Println(err)
				os.Exit(1)
			}
		}

	},
}

func init() {
	rootCmd.AddCommand(calcCmd)

	// Here you will define your flags and configuration settings.

	// Cobra supports Persistent Flags which will work for this command
	// and all subcommands, e.g.:
	// calcCmd.PersistentFlags().String("foo", "", "A help for foo")

	// Cobra supports local flags which will only run when this command
	// is called directly, e.g.:
	// calcCmd.Flags().BoolP("toggle", "t", false, "Help message for toggle")
}
