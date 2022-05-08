

topics

lvl1/lvl2/thing/purpose


thing - rpi, fan1, light1, ... (except rpi everyother things should be mentioned in state.json) \
purpose - status(if published an empty message rpi will reply whether it is on/off),
		state( to change the state to on/off),
		statusreply(topic on which rpi willreply)


for eg 

On Publishing empty message on topic emblab/iotremote/rpi/status

Rpi will reply in topic emblab/iotremote/rpi/statusreply  with payload "rpi is connected"


On Publishing empty message on topic emblab/iotremote/fan1/status

Rpi will reply in topic emblab/iotremote/rpi/statusreply  with payload "on" / "off"

To change state of fan1, 

Publish on/off in the topic  emblab/iotremote/fan1/on

if rpi disconnected due to powercut off 

lastwill message will be published on topic emblab/iotremote/rpi/statusreply with payload "rpi is disconnected"
