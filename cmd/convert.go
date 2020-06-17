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

	"github.com/spf13/cobra"
	"github.com/timdrysdale/gorad/grfile"
	"github.com/timdrysdale/gorad/lvfile"
	"github.com/timdrysdale/gorad/util"
)

// convertCmd represents the convert command
var convertCmd = &cobra.Command{
	Use:   "convert [input-dir] [output-dir]",
	Short: "Produce data files that contain all points for a given frequency",
	Args:  cobra.ExactArgs(2),
	Long: `Read in all .dat files in a given directory, and produce a set of files 
with one file for each frequency, in that data set.`,
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("convert called")

		inputDir := os.Args[2]
		outputDir := os.Args[3]

		samples, err := lvfile.ParseDATDir(inputDir)

		if err != nil {
			fmt.Println(err)
			os.Exit(1)

		}

		util.EnsureDirAll(outputDir)

		err = grfile.WriteByFreq(samples, outputDir)

	},
}

func init() {
	rootCmd.AddCommand(convertCmd)

	// Here you will define your flags and configuration settings.

	// Cobra supports Persistent Flags which will work for this command
	// and all subcommands, e.g.:
	// convertCmd.PersistentFlags().String("foo", "", "A help for foo")

	// Cobra supports local flags which will only run when this command
	// is called directly, e.g.:
	// convertCmd.Flags().BoolP("toggle", "t", false, "Help message for toggle")
}
