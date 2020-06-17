package grfile

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"

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
