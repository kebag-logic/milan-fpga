# AEM and AECP

## Introduction

The ATDECC Entity Model, is the modelled representation of what a network system's abilities. This is meant to be static for every system as an initial state. However, it provides a way to configure a system, allowing some flexibility, and permit inter-operabilities between systems so that they can understand each other.

In addition, to the AEM, the AECP, [ATDECC Enumeration and Control Protocol](https://kebag-logic.com/redirect-index-2532176562193/docs/link/102#bkmrk-page-title), allows every ATDECC compliant devices to communicate their entity model to each other. AECP is not only transferring AEM descriptors, but also provides a controller to take action on the system via its entity model's descriptor.

## Scope

The objective is to list what would be necessary to have to comply with the [initial specifications](https://kebag-logic.com/redirect-index-2532176562193/docs/link/46#bkmrk-avb%2Fmilan). Here, the FPGA and some software control will be discussed.

## ATDECC Enumeration and Control Protocol specification

The system needs to implement the necessary state machine as described in the [standard dissection](https://kebag-logic.com/redirect-index-2532176562193/docs/books/standards-dissection/page/atdecc-enumaration-and-control-protocol-aecp) section.

### State machines to implement:

The following state machines shall be implemented:

- The AECP [ state machine](https://kebag-logic.com/redirect-index-2532176562193/docs/link/102#bkmrk-%C2%A0-%C2%A0-3.4.3.5-state-ma) for the ATDECC commands
- The AECP [Vendor Unique Command](https://kebag-logic.com/redirect-index-2532176562193/docs/link/102#bkmrk-vendor-unique-format) for Milan: 
    - Protocol ID: 00-1B-C5-0A-C1-00
    - GET\_ MILAN\_INFO
    - GET/SET\_SYSTEM\_UNIQUE\_ID
    - GET/SET\_MEDIA\_CLOCK\_REFERENCE\_INFO

## Entity model technical specs

An entity model is a challenging thing to create inside logic. For the sake of simplicity, the entity model will be minimalistic to cover a talker and listener, starting with the latter.

### Entity

#### Static information

- **Because of AVB,** only one entity
- The entity ID is unique, and shall be derived from the MAC address
- 3 Stored configurations, only one activate at the time: 
    - Raki - 48 kHz
    - Raki - 96 kHz
    - Raki - 192 kHz

#### Dynamic information

The dynamic information, modelized as variables (metadata), necessary for the entity would be:

<table border="1" id="bkmrk-command-name-variabl-1" style="border-collapse: collapse; width: 100%; height: 255.7px;"><colgroup><col style="width: 37.6512%;"></col><col style="width: 33.001%;"></col><col style="width: 29.4332%;"></col></colgroup><thead><tr style="height: 29.55px;"><td style="height: 29.55px;">Command Name</td><td style="height: 29.55px;">Variable</td><td style="height: 29.55px;">Attributes of the variable</td></tr></thead><tbody><tr style="height: 107.95px;"><td style="height: 107.95px;">SET-GET \_CONFIGURATION</td><td style="height: 107.95px;">A pointer to the current configuration index.

The configuration ID change, 3 configurations as per the [Entity Configuration Section](https://kebag-logic.com/redirect-index-2532176562193/docs/link/117#bkmrk-entity-configuration)

</td><td style="height: 107.95px;">- NONVOLATILE
- RESETTABLE

</td></tr><tr style="height: 29.55px;"><td style="height: 29.55px;">DE/REGISTER\_UNSOLICITED\_NOTIFICATION</td><td style="height: 29.55px;">**Table of 16 controllers ID 64 bit long**</td><td style="height: 29.55px;">  
</td></tr><tr style="height: 29.55px;"><td style="height: 29.55px;">LOCK\_ENTITY</td><td style="height: 29.55px;">A boolean providing the information whether it is linked or not  
</td><td style="height: 29.55px;">- TIMEOUTS

</td></tr><tr style="height: 29.55px;"><td style="height: 29.55px;">  
</td><td style="height: 29.55px;">  
</td><td style="height: 29.55px;">  
</td></tr><tr style="height: 29.55px;"><td style="height: 29.55px;">  
</td><td style="height: 29.55px;">  
</td><td style="height: 29.55px;">  
</td></tr></tbody></table>

### Entity configuration

Three configurations may be supported, for the following sample rate: 192 kHz, 96 kHz and 48 kHz.

#### Static information

<table border="1" id="bkmrk-descriptor-type-coun-1" style="border-collapse: collapse; width: 100%; height: 407.55px;"><colgroup><col style="width: 33.3333%;"></col><col style="width: 33.3333%;"></col><col style="width: 33.3333%;"></col></colgroup><thead><tr style="height: 29.55px;"><td style="height: 29.55px;">Descriptor type</td><td style="height: 29.55px;">Counts</td><td style="height: 29.55px;">Notes</td></tr></thead><tbody><tr style="height: 69.8px;"><td style="height: 69.8px;">STREAM\_INPUT</td><td style="height: 69.8px;">2 Streams input</td><td style="height: 69.8px;">- 1 AAF Stream
- 1 CRF Stream

</td></tr><tr style="height: 69.8px;"><td style="height: 69.8px;">STREAM\_OUTPUT</td><td style="height: 69.8px;">2 Stream outputs</td><td style="height: 69.8px;">- 1 AAF Stream
- 1 CRF Stream

</td></tr><tr style="height: 29.55px;"><td style="height: 29.55px;">AVB\_INTERFACE</td><td style="height: 29.55px;">1 network interface</td><td style="height: 29.55px;">  
</td></tr><tr style="height: 29.55px;"><td style="height: 29.55px;">CLOCK\_DOMAIN</td><td style="height: 29.55px;">1 clock domain</td><td style="height: 29.55px;">  
</td></tr><tr style="height: 86.6px;"><td style="height: 86.6px;">CLOCK\_SOURCES</td><td style="height: 86.6px;">3 clock sources</td><td style="height: 86.6px;">- 1 Internal
- 1 AAF Stream derived
- 1 CRF Stream derived

</td></tr><tr style="height: 63.15px;"><td style="height: 63.15px;">AUDIO\_UNIT</td><td style="height: 63.15px;">1 audio unit for the input and output streams and input and output clusters available</td><td style="height: 63.15px;"></td></tr><tr style="height: 29.55px;"><td style="height: 29.55px;">STREAM\_PORT\_INPUT</td><td style="height: 29.55px;">1 Stream output port</td><td style="height: 29.55px;"></td></tr><tr><td>AUDIO\_CLUSTER</td><td>16 Audio clusters:  
- 8 input audio clusters
- 8 output audio clusters

</td><td></td></tr><tr><td>AUDIO\_MAP</td><td>None, everything can be dynamic  
</td><td></td></tr><tr><td>CONTROL</td><td>1   
</td><td>Identity control.

</td></tr></tbody></table>

#### Dynamic information

<p class="callout danger">TODO</p>

### Non-Volatile information

The following information should be saved, and resettable upon device factory-reset.

## FPGA

The FPGA implementation needs to provide flexibility for development and for the end-user. As a consequence, this raises multiple questions:

1. How to make the FPGA's entity descriptor flexible --&gt; Yes up to a certain size
2. How to make the getter/setter generics to avoid code duplication
3. How to manage static, semi-static and dynamic info differently within the same descriptor
4. Ensure a Factory reset and Non-Volatile updates.

### Solution

In order to, cope with the aforementioned issues, the following solutions would be necessary:

- A 4 level multi-level Block descriptions
- A generic Getter/Setter select to allow read/write of the necessary payload.
- An alias memory mapped for dynamically parameters, static, and semi-static
- A read-only, Factory defined Non-volatile memory
- A Modifiable a read/write Non-volatile memory overlaying the factory.
- A Volatile read/write for fast access, mirroring the modifiable read/write overlay.

#### The 4-Level block description

The Diagram below describes the 4-level block description, similar to a file system, it will handle memory-based Entity Model descriptors. There is **only one 4-level memory block descriptor per** entity.

<div drawio-diagram="519"><img src="https://kebag-logic.com/redirect-index-2532176562193/docs/uploads/images/drawio/2025-06/WGvlLYbV58TAXnXo-drawing-1-1749020003.png" alt=""/></div>

<table border="1" id="bkmrk-level-description-le-1" style="border-collapse: collapse; width: 100%; height: 467.784px;"><colgroup><col style="width: 50%;"></col><col style="width: 50%;"></col></colgroup><thead><tr style="height: 29.7167px;"><td style="height: 29.7167px;">Level</td><td style="height: 29.7167px;">Description</td></tr></thead><tbody><tr style="height: 46.5167px;"><td style="height: 46.5167px;">Level 0</td><td style="height: 46.5167px;"> This is the **ENTITY** that holds information necessary to be parsed.

</td></tr><tr style="height: 63.3167px;"><td style="height: 63.3167px;">Level 1</td><td style="height: 63.3167px;">The level 0 BLOCK contains a list of address ordered by descriptor ID starting from the **CONFIGURATION descriptor.**

**It lives in the RAM / BLOCK\_RAM.**

</td></tr><tr style="height: 147.317px;"><td style="height: 147.317px;">Level 2</td><td style="height: 147.317px;">The level 1 contains multiple tables. Each table is made the same with the first position the number of descriptor (count), referring to the **Descriptor INDEX**.

Other position in the table are addresses where are located the payload of the descriptor.

**It lives in the RAM / BLOCK\_RAM.**

</td></tr><tr style="height: 180.917px;"><td style="height: 180.917px;">Level 3</td><td style="height: 180.917px;">The deepest level contains the size of the payload.  
The first place in the array contains the size of the "static, semi-static" data"

The second place contains the size of the dynamic array.

The Payload corresponds to the 1722.1 descriptor information held in the memory.

The dynamic Address is mapped to a Multiplexed registered data.

  
Everything **lives in the RAM / BLOCK\_RAM. Except where the dynamic data is pointing to.**

</td></tr></tbody></table>

Addresses are 16 bits, in the case when bigger than 16 bits addresses are used, they are done modulo the size of the bigger size, i.e:

- In the 32 bits are used, use an offset, and work in this offset aligned on a 16 bits boundaries.

#### A generic Getter/Setter

The generic Getter/Setter would allow for parsing and generate an accessor to access a specific descriptor in the memory. Based on the information from a getter setter as described in the [ATDECC Entity Model section,](https://kebag-logic.com/redirect-index-2532176562193/docs/link/22#bkmrk--47) there is some information to gather to access the 3-level block memory:

<table border="1" id="bkmrk-information-accessor-1" style="border-collapse: collapse; width: 100%; height: 828.985px;"><colgroup><col style="width: 18.2335%;"></col><col style="width: 25.9797%;"></col><col style="width: 19.6665%;"></col><col style="width: 36.2256%;"></col></colgroup><thead><tr style="height: 46.5167px;"><td style="height: 46.5167px;">Information Accessor from</td><td style="height: 46.5167px;">Part of</td><td style="height: 46.5167px;">Level Accessed information</td><td style="height: 46.5167px;">Command/Response access </td></tr></thead><tbody><tr style="height: 155.767px;"><td style="height: 155.767px;">**command\_type**</td><td style="height: 155.767px;">AECP Common Data</td><td style="height: 155.767px;">For command that only have this System information.

**Level 0 Access**

</td><td style="height: 155.767px;">- ACQUIRE\_ENTITY(ONLY this parameter)
- LOCK\_ENTITY(ONLY this parameter)
- ENTITY\_AVAILABLE (ONLY this parameter)
- The rest of the Commands uses it.

</td></tr><tr style="height: 174.367px;"><td style="height: 174.367px;">**conﬁguration\_index**</td><td style="height: 174.367px;">AECP Message-Specific Data</td><td style="height: 174.367px;">**Level 1 Access**</td><td style="height: 174.367px;">- READ\_DESCRIPTOR
- WRITE\_DESCRIPTOR
- GET\_CONFIGURATION
- SET\_CONFIGURATION
- GET\_NAME
- SET\_NAME
- GET\_ASSOCIATION\_ID
- SET\_ASSOCIATION\_ID

</td></tr><tr style="height: 242.917px;"><td style="height: 242.917px;">**descriptor\_type**</td><td style="height: 242.917px;">AECP Message-Specific Data</td><td style="height: 242.917px;">**Level 2 access**</td><td style="height: 242.917px;">All Except:

- GET\_CONFIGURATION
- SET\_CONFIGURATION
- GET\_ASSOCIATION\_ID
- SET\_ASSOCIATION\_ID
- REGISTER\_UNSOL..
- DEREGISTER\_UNSOL..
- GET\_AS\_PATH
- AUTH\_XXX
- ENABLE\_TRANSPORT\_SECURITY
- GET\_DYNAMIC\_INFO
- 

</td></tr><tr style="height: 209.417px;"><td style="height: 209.417px;">**descriptor\_index**</td><td style="height: 209.417px;">AECP Message-Specific Data</td><td style="height: 209.417px;">**Level 3 access**</td><td style="height: 209.417px;">All Except:

- GET\_CONFIGURATION
- SET\_CONFIGURATION
- GET\_ASSOCIATION\_ID
- SET\_ASSOCIATION\_ID
- REGISTER\_UNSOL..
- DEREGISTER\_UNSOL..
- AUTH\_XXX
- ENABLE\_TRANSPORT\_SECURITY
- 

</td></tr></tbody></table>

### Overall Design of the volatile part

The design below aims to describe how the internal block will handle access of the different descriptor and internal states of the AECP processing Unit.

<div drawio-diagram="518"><img src="https://kebag-logic.com/redirect-index-2532176562193/docs/uploads/images/drawio/2025-06/6OK2GjpcII4TAnbq-drawing-1-1748847387.png" alt=""/></div>

<p class="callout danger">TODO ADD the interaction with the filtering database, using the AVAILABLE messages for UC traffic. ==&gt; Done via the AECP Memory mapped.</p>

#### AECP Packet Validation

##### Expected behaviour

- The AECP packet validation makes sure that packet **control\_data\_lenght** corresponds to the packet.
- The AECP **message\_type** corresponds to the **AEM\_COMMAND (0)**
- The AECP's **status** is **SUCCESS (0)**
- <span style="color: rgb(224, 62, 45);">Fails when none of the written above checks pass.</span>
    - <span style="color: rgb(224, 62, 45);">Error message's is the AECP's status response. And it would be **BAD\_ARGUMENTS (7)**</span>

#### AECP Common Data Parser

##### Expected behaviour

- Extracts the **target\_entity\_id** from the **AECP Common Data**
- Extracts the **command\_type** from the **AECP Common Data**
- Checks the **command\_type** validity
- Checks the **controller\_id**
- <span style="color: rgb(224, 62, 45);">Fails when:</span>
    - <span style="color: rgb(224, 62, 45);">The command\_type does not exist.</span>

#### AECP Command Specific Extract

##### Expected behaviour

- From the Command specific part, and according to the table referred in section [A generic Getter/Setter](https://kebag-logic.com/redirect-index-2532176562193/docs/link/117#bkmrk-a-generic-getter%2Fset), pass an offset in the packet and validity signal: 
    - The offset and validity of the **configuration\_index** within the packet
    - The offset and validity of the **descriptor\_type** within the packet
    - The offset and validity of the **descriptor\_index** within the packet
- Provides to the AEM whether it is a **getter or setter.**
- Provides whether this command expects to send **Unsolicited** notification or not.
- <span style="color: rgb(224, 62, 45);">Fails, when :</span>
    - <span style="color: rgb(224, 62, 45);">The **target\_entity\_id** is not equal to **Current Selected configuration,** **L0, BAD\_ARGUMENTS (7) (TODO verify with the spec)**</span>
    - <span style="color: rgb(224, 62, 45);">The command\_type is not supported. Error code is **NOT\_IMPLEMENTED (1)**</span>
    - <span style="color: rgb(224, 62, 45);">The entity is locked and if the command does not perform when the entity is locked, then the command returns **ENTITY\_LOCKED (3)**</span>

#### AECP L0 Current Selected Configuration

##### Expected behaviour

- At all time, provide the information about: 
    - The **current\_configuration**
    - The **current\_endity\_id**
- <span style="color: rgb(224, 62, 45);">If none of these are available for any reason</span>
    - <span style="color: rgb(224, 62, 45);">Return a message with ENTITY\_MISBEHAVING</span>

#### AECP Specific Data Parser

##### Expected behaviour

- If enabled: 
    - Pass down the parameters Valid and Index information
    - The **configuration\_index** validity will behave differently to comply with the 1722.1 Specification
    - If the packet is a **command\_type** of **SET/GET\_CONFIGURATION,** then it will use the packet's **configuration\_index** information
    - Otherwise it will use L0 current status
- <span style="color: rgb(224, 62, 45);">Otherwise:</span>
    - <span style="color: rgb(224, 62, 45);">Do not care about the values,</span>
    - <span style="color: rgb(224, 62, 45);">Make sure the Enable signals are set to 0.</span>

#### AECP Packet response

##### Expected behaviour

- Buffer the entire packet
- Adds the necessary payload depending on **command\_type**. 
    - For the **SETTER**, the same payload is returned.
    - For the **GETTER** the same packet should be returned, with the added state of the memory.
- Adds the **status** provided from the upstream modules (Any Status code, error, or success)
- Set the **message\_type** set 
    - AEM\_RESPONSE
    - VENDOR\_UNIQUE\_RESPONSE if a vendor unique

#### AECP Unsolicited / Change Request notifications

##### Expected behaviour

- The system can keep up to 16 Controller\_ID in the L0 **Dynamic** memory of the system
- A Signal from the [AECP Command Specific Extract](https://kebag-logic.com/redirect-index-2532176562193/docs/link/117#bkmrk-aecp-unsolicited-%2F-c) whether it is unsolicited or not.

#### AECP Timers

##### Expected behaviour

- The timer shall provide a timeout for: 
    - The 1-minute timeout from the ENTITY\_LOCK command, Unlocks after the 1-second
- Shall provide a 1-second throttle mechanism upon GET\_COUNTER updates from internal counters.
- Unsolicited/Solicited, remove from the DB after not receiving AVAILBLE\_CONTROLLER for some time.

### AECP Memory Mapped module

<p class="callout danger">TODO: Provide the AECP MEMORY MAPPED module dependent on the descriptor and the configuration of a descriptor.</p>

The list of the different data that are directly linked to a MILAN/AVB descriptor, and as a result dependent on commands or unsolicited-notification such as **GET\_COUNTERS:**

- Stream Port IN/OUT 
    - The specified Milan and AVB counter value.
    - Mappings with the Audio Unit to the Stream Port via the Audio Cluster configuration
- Stream IN/OUT 
    - Format
    - Asynchronous Rate Converters
- Audio Units
- Milan Network interface: 
    - Milan and AVB counter value.
- Identifying
- All the module supporting the CR (change request).
- Filtering database, reacting to the **AVAILABLE\_CONTROLLER** message to use the **Unicast** rather than the **Multicast**.
- Database of the Controller
- PTP information

All the modules above need to be memory mapped to a specific **DESCRIPTOR**. That's part of the **DYNAMIC** information map from the **AEM\_MEMORY**.