# Process SalesForce Visual Force Labels!

## How to use
- In your Visual Force page, have your labels like this: `<p>{_"Hi there I'm a label"_}</p>`
- Run `Process SalesForce Labels` in the Sublime Command palette
- Magic!
	- The plugin replaces the labels with VisualForce syntax
	- If they're not in the labels file already, its being added

## Installation
- Copy the `processSfLabels` folder into `~/Library/Application Support/Sublime Text 3/Packages/`
- Make sure you have a XML file at `src/labels/CustomLabels.labels`
- Make sure you work within an opened MavensMate project