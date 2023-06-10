import sys
import toolutils

outputitem = None
inputindex = -1
inputitem = None
outputindex = -1

num_args = 1
h_extra_args = ''
pane = toolutils.activePane(kwargs)
if not isinstance(pane, hou.NetworkEditor):
    pane = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    if pane is None:
       hou.ui.displayMessage(
               'Cannot create node: cannot find any network pane')
       sys.exit(0)
else: # We're creating this tool from the TAB menu inside a network editor
    pane_node = pane.pwd()
    if "outputnodename" in kwargs and "inputindex" in kwargs:
        outputitem = pane_node.item(kwargs["outputnodename"])
        inputindex = kwargs["inputindex"]
        h_extra_args += 'set arg4 = "' + kwargs["outputnodename"] + '"\n'
        h_extra_args += 'set arg5 = "' + str(inputindex) + '"\n'
        num_args = 6
    if "inputnodename" in kwargs and "outputindex" in kwargs:
        inputitem = pane_node.item(kwargs["inputnodename"])
        outputindex = kwargs["outputindex"]
        h_extra_args += 'set arg6 = "' + kwargs["inputnodename"] + '"\n'
        h_extra_args += 'set arg9 = "' + str(outputindex) + '"\n'
        num_args = 9
    if "autoplace" in kwargs:
        autoplace = kwargs["autoplace"]
    else:
        autoplace = False
    # If shift-clicked we want to auto append to the current
    # node
    if "shiftclick" in kwargs and kwargs["shiftclick"]:
        if inputitem is None:
            inputitem = pane.currentNode()
            outputindex = 0
    if "nodepositionx" in kwargs and             "nodepositiony" in kwargs:
        try:
            pos = [ float( kwargs["nodepositionx"] ),
                    float( kwargs["nodepositiony"] )]
        except:
            pos = None
    else:
        pos = None

    if not autoplace and not pane.listMode():
        if pos is not None:
            pass
        elif outputitem is None:
            pos = pane.selectPosition(inputitem, outputindex, None, -1)
        else:
            pos = pane.selectPosition(inputitem, outputindex,
                                      outputitem, inputindex)

    if pos is not None:
        if "node_bbox" in kwargs:
            size = kwargs["node_bbox"]
            pos[0] -= size[0] / 2
            pos[1] -= size[1] / 2
        else:
            pos[0] -= 0.573625
            pos[1] -= 0.220625
        h_extra_args += 'set arg2 = "' + str(pos[0]) + '"\n'
        h_extra_args += 'set arg3 = "' + str(pos[1]) + '"\n'
h_extra_args += 'set argc = "' + str(num_args) + '"\n'

pane_node = pane.pwd()
child_type = pane_node.childTypeCategory().nodeTypes()

if 'chopnet' not in child_type:
   hou.ui.displayMessage(
           'Cannot create node: incompatible pane network type')
   sys.exit(0)

# First clear the node selection
pane_node.setSelected(False, True)

h_path = pane_node.path()
h_preamble = 'set arg1 = "' + h_path + '"\n'
h_cmd = r'''
if ($argc < 2 || "$arg2" == "") then
   set arg2 = 0
endif
if ($argc < 3 || "$arg3" == "") then
   set arg3 = 0
endif
# Automatically generated script
# $arg1 - the path to add this node
# $arg2 - x position of the tile
# $arg3 - y position of the tile
# $arg4 - input node to wire to
# $arg5 - which input to wire to
# $arg6 - output node to wire to
# $arg7 - the type of this node
# $arg8 - the node is an indirect input
# $arg9 - index of output from $arg6

\set noalias = 1
set saved_path = `execute("oppwf")`
opcf $arg1

# Node $_obj_RETIME (Object/chopnet)
set _obj_RETIME = `run("opadd -e -n -v chopnet RETIME")`
oplocate -x `$arg2 + 0` -y `$arg3 + 0` $_obj_RETIME
opspareds '    parm {         name    "origcamera"         label   "Original Camera"         type    oppath         default { "../ORIG_CAM" }         parmtag { "oprelative" "." }         parmtag { "script_callback_language" "python" }     }     parm {         name    "newcamera"         label   "New Camera"         type    oppath         default { "../RETIME_CAM" }         parmtag { "oprelative" "." }         parmtag { "script_callback_language" "python" }     }     parm {         name    "retimefactor"         label   "Retime Factor"         type    float         default { "1" }         range   { 0 10 }         parmtag { "script_callback_language" "python" }     } ' $_obj_RETIME
opcolor -c 0.28999999165534973 0.56499999761581421 0.88599997758865356 $_obj_RETIME
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F off -c on -e on -b off $_obj_RETIME
opexprlanguage -s hscript $_obj_RETIME
opuserdata -n '___Version___' -v '19.0.383' $_obj_RETIME
opuserdata -n 'nodeshape' -v 'camera' $_obj_RETIME
opcf $_obj_RETIME

# Node $_obj_RETIME_retime_stretch (Chop/stretch)
set _obj_RETIME_retime_stretch = `run("opadd -e -n -v stretch retime_stretch")`
oplocate -x `$arg2 + -251.548` -y `$arg3 + 50.289999999999999` $_obj_RETIME_retime_stretch
chblockbegin
chadd -t 0 0 $_obj_RETIME_retime_stretch end
chkey -t 0 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../retimefactor")' $_obj_RETIME_retime_stretch/end
chblockend
opparm -V 19.0.383 $_obj_RETIME_retime_stretch end ( end ) gcolor ( 0 0.44999998807907104 0.89999997615814209 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -a off -o off $_obj_RETIME_retime_stretch
opexprlanguage -s hscript $_obj_RETIME_retime_stretch
opuserdata -n '___Version___' -v '19.0.383' $_obj_RETIME_retime_stretch

# Node $_obj_RETIME_export_to_retime_cam (Chop/export)
set _obj_RETIME_export_to_retime_cam = `run("opadd -e -n -v export export_to_retime_cam")`
oplocate -x `$arg2 + -251.548` -y `$arg3 + 49.160499999999999` $_obj_RETIME_export_to_retime_cam
opparm -V 19.0.383 $_obj_RETIME_export_to_retime_cam channels ( 'rx ry rz tx ty tz' ) nodepath ( '`chsop("../newcamera")`' ) path ( 'rx ry rz tx ty tz' ) gcolor ( 0.44999998807907104 0 0.89999997615814209 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -a on -o on $_obj_RETIME_export_to_retime_cam
opexprlanguage -s hscript $_obj_RETIME_export_to_retime_cam
opuserdata -n '___Version___' -v '19.0.383' $_obj_RETIME_export_to_retime_cam

# Node $_obj_RETIME_in_cam (Chop/fetch)
set _obj_RETIME_in_cam = `run("opadd -e -n -v fetch in_cam")`
oplocate -x `$arg2 + -251.548` -y `$arg3 + 51.419499999999999` $_obj_RETIME_in_cam
opparm -V 19.0.383 $_obj_RETIME_in_cam nodepath ( '`chsop("../origcamera")`' ) path ( 'tx ty tz rx ry rz' ) rate ( 25 ) gcolor ( 0.89999997615814209 0 0.44999998807907104 )
opset -d off -r on -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -a off -o off $_obj_RETIME_in_cam
opexprlanguage -s hscript $_obj_RETIME_in_cam
opuserdata -n '___Version___' -v '19.0.383' $_obj_RETIME_in_cam
oporder -e retime_stretch export_to_retime_cam in_cam 
opcf ..
opset -p on $_obj_RETIME

opcf $arg1
opcf $_obj_RETIME
opwire -n $_obj_RETIME_in_cam -0 $_obj_RETIME_retime_stretch
opwire -n $_obj_RETIME_retime_stretch -0 $_obj_RETIME_export_to_retime_cam
opcf ..

set oidx = 0
if ($argc >= 9 && "$arg9" != "") then
    set oidx = $arg9
endif

if ($argc >= 5 && "$arg4" != "") then
    set output = $_obj_RETIME
    opwire -n $output -$arg5 $arg4
endif
if ($argc >= 6 && "$arg6" != "") then
    set input = $_obj_RETIME
    if ($arg8) then
        opwire -n -i $arg6 -0 $input
    else
        opwire -n -o $oidx $arg6 -0 $input
    endif
endif
opcf $saved_path
'''
hou.hscript(h_preamble + h_extra_args + h_cmd)
