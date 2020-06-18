package grfile

import (
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"strings"

	mgl "github.com/go-gl/mathgl/mgl64"
	"github.com/gocarina/gocsv"
	"github.com/timdrysdale/gorad/core"
)

func WriteByFreq(samples []core.Sample, outputDir string) error {

	sampleMap := make(map[int]*[]core.Sample)

	for _, sample := range samples {

		key := sample.Freq

		if _, ok := sampleMap[key]; !ok {
			sampleMap[key] = &[]core.Sample{}
		}

		*sampleMap[sample.Freq] = append(*sampleMap[sample.Freq], sample)

	}

	for freq, sampleList := range sampleMap {

		filename := fmt.Sprintf("%d-freq.csv", freq)

		fullPath := filepath.Join(outputDir, filename)

		file, err := os.OpenFile(fullPath, os.O_RDWR|os.O_CREATE, os.ModePerm)
		if err != nil {
			panic(err)
		}

		fileSamples := ConvertSamplesToFileSamples(*sampleList)

		err = gocsv.MarshalFile(&fileSamples, file)

		file.Close()

		if err != nil {
			return err
		}

	}

	return nil

}

func SaveResults(result *core.Calc, dir string) error {

	rf := result.Setup

	filename := fmt.Sprintf("%s-%d-%g-%g-%d-results.csv", rf.Plane, rf.Freq, rf.Intersect, rf.Width, rf.Points)
	fullPath := filepath.Join(dir, filename)
	if result.Farfields == nil {
		return errors.New("nil pointer to results")
	}
	fileSamples := ConvertSamplesToFileSamples(*result.Farfields)
	file, err := os.OpenFile(fullPath, os.O_RDWR|os.O_CREATE, os.ModePerm)
	if err != nil {
		panic(err)
	}
	err = gocsv.MarshalFile(&fileSamples, file)

	file.Close()

	if err == nil {
		fmt.Println(fullPath)
	}

	return err

}

func ReadFreq(path string) ([]core.Sample, error) {

	samples := []core.Sample{}

	file, err := os.Open(path)
	if err != nil {
		return samples, err
	}

	defer file.Close()

	fileSamples := []core.FileSample{}

	err = gocsv.UnmarshalFile(file, &fileSamples)

	if err != nil {
		return samples, err
	}

	samples = ConvertFileSamplesToSamples(fileSamples)

	return samples, nil

}

func ConvertSamplesToFileSamples(samples []core.Sample) []core.FileSample {

	fileSamples := []core.FileSample{}

	for _, sample := range samples {

		fileSamples = append(fileSamples, core.FileSample{
			Freq: sample.Freq,
			X:    sample.Pos.X(),
			Y:    sample.Pos.Y(),
			Z:    sample.Pos.Z(),
			Real: real(sample.Val),
			Imag: imag(sample.Val),
		})

	}

	return fileSamples

}

func ConvertFileSamplesToSamples(filesamples []core.FileSample) []core.Sample {

	samples := []core.Sample{}

	for _, fs := range filesamples {

		samples = append(samples, core.Sample{
			Freq: fs.Freq,
			Pos:  mgl.Vec3{fs.X, fs.Y, fs.Z},
			Val:  complex(fs.Real, fs.Imag),
		})

	}

	return samples

}

func ReadFarfields(path string) ([]*core.Farfield, error) {

	farfields := []*core.Farfield{}

	file, err := os.Open(path)
	if err != nil {
		return farfields, err
	}

	defer file.Close()

	if err := gocsv.UnmarshalFile(file, &farfields); err != nil {
		panic(err)
	}

	for idx, farfield := range farfields {
		farfields[idx].Plane = strings.TrimSpace(farfield.Plane)
	}

	return farfields, nil
}
