# Python API for building CatalystML

This is a tool for creating a CML JSON structure within python.  This was created for use with python3.6+

## Use

To create a CML JSON you need to import the cmlmaker.py package:

```
import cmlmaker as cml
```

Then declare a cml structure and add an input (a map called df):
```
cs = cml.structure("Title","Description of JSON)
cs = cs.addInput(cml.inobj("map","df"))
```
Then adding an operation:
```
cs = cs.addOp(cml.normalize(cml.normalize.inputs(data="$df['Age']",value=100,minval=18),output="df['Age']"))

cols2keep=["ATM","Age","AmEx","Amount","Bank0"]

cs=cs.addOp(cml.ops.restructuring.map2table(cml.map2table.inputs("$df",cols2keep),output="datatab"))

```
Repeat until all operations have been added.  The include an output:
```
cs=cs.addOutput(cml.outobj("array","$datatab"))
```

Print json:
```
print(cs)
```

Writing to file:
```
cs.writeToFile('output_file.json')
```

