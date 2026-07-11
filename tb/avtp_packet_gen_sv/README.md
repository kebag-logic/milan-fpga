# Docs

https://drive.google.com/drive/folders/1cpxTL89wJGm4jEeFQBAxymLb1budsLeG

# Objective

The aim is to create random AVTP ethernet packet in sv environment.


# Usage for Modelsim/Questa

* Launch the vsim on terminal
* Navigate to the avtp_packet_gen folder
* Run the "do run.do" command on Modelsim/Questa

```
./vsim 
cd $REPO_PATH/tb/avtp_packet_gen_sv/examples
do run.do
```

# Notes

1. In order to use free version of the Modelsim/Questa, **randomize()** method has not been used. Instead, custom logic for randomization has been developed.
2. This folder is still in development phase.
3. At the moment, it is desinged for Modelsim/Questa. The AMD Vivado support will be added.
