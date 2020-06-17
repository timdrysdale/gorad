package lvfile

import (
	"bufio"
	"errors"
	"os"
	"path/filepath"
	"regexp"
	"strconv"
	"strings"

	mgl "github.com/go-gl/mathgl/mgl64"
)

type Sample struct {
	Pos  mgl.Vec3
	Freq float64
	Val  complex128
}

func GetFileList(dir string) ([]string, error) {

	paths := []string{}

	err := filepath.Walk(dir, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}

		if !info.IsDir() {
			paths = append(paths, path)
		}

		return nil
	})

	return paths, err

}

func IsDAT(path string) bool {
	suffix := strings.ToLower(filepath.Ext(path))
	return strings.Compare(suffix, ".dat") == 0
}

func ParseDATFile(inputPath string) ([]Sample, error) {

	pos := mgl.Vec3{}

	samples := []Sample{}

	file, err := os.Open(inputPath)

	if err != nil {
		return samples, err
	}

	defer file.Close()

	scanner := bufio.NewScanner(file)

SCAN:
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())

		//use for case insenstive field identification only
		//need to keep capitalisation in filenames
		lline := strings.ToUpper(line)

		switch {
		case strings.HasPrefix(lline, "TITLE:"):
			pos, err = ProcessTitle(line)
			if err != nil {
				return samples, err
			}

		case strings.HasPrefix(lline, "STIMULUS, REAL, IMAGINARY"):
			break SCAN
		default:
			continue
		}
	}

	// now read in the samples ....
	// modified from https://www.regular-expressions.info/floatingpoint.html
	re := regexp.MustCompile("([-+]?[0-9]*\\.?[0-9]+(?:[eE][-+]?[0-9]+))")

	for scanner.Scan() {

		line := scanner.Text()
		tokens := re.FindAllStringSubmatch(line, -1)

		if len(tokens) == 3 {

			freq, err := strconv.ParseFloat(tokens[0][0], 64)
			if err != nil {
				continue
			}

			real, err := strconv.ParseFloat(tokens[1][0], 64)
			if err != nil {
				continue
			}

			imag, err := strconv.ParseFloat(tokens[2][0], 64)
			if err != nil {
				continue
			}

			samples = append(samples, Sample{
				Pos:  pos,
				Freq: freq,
				Val:  complex(real, imag),
			})

		}

	}

	return samples, scanner.Err()
}

func ProcessTitle(line string) (mgl.Vec3, error) {

	re := regexp.MustCompile("x=\\s*([-+]?[0-9]*\\.?[0-9]*).*y=\\s*([-+]?[0-9]*\\.?[0-9]*).*z=\\s*([-+]?[0-9]*\\.?[0-9]*)")

	tokens := re.FindStringSubmatch(line)

	if len(tokens) == 4 {

		x, err := strconv.ParseFloat(tokens[1], 64)

		if err != nil {
			return mgl.Vec3{}, errors.New("Unexpected Title Format")
		}
		y, err := strconv.ParseFloat(tokens[2], 64)

		if err != nil {
			return mgl.Vec3{}, errors.New("Unexpected Title Format")
		}

		z, err := strconv.ParseFloat(tokens[3], 64)

		if err != nil {
			return mgl.Vec3{}, errors.New("Unexpected Title Format")
		}

		return mgl.Vec3{x, y, z}, nil
	}

	return mgl.Vec3{}, errors.New("Unexpected Title Format")
}
