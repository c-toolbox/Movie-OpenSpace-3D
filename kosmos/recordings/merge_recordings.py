import sys

class Frame:
  TypeCamera = 'camera'
  TypeScript = 'script'

  frame_type = ''
  timeOs = -1.0
  timeRec = -1.0
  timeSim = -1.0

  # If camera frame
  position_x = -1.0
  position_y = -1.0
  position_z = -1.0
  rotation_x = -1.0
  rotation_y = -1.0
  rotation_z = -1.0
  rotation_w = -1.0
  scale = -1.0
  rotation_following = False
  focus_node = ''

  # If script frame
  script = ''

  def __init__(self, line):
    if line == '':
      return

    comp = line.split(' ')

    self.frame_type = comp[0]
    self.timeOs = float(comp[1])
    self.timeRec = float(comp[2])
    self.timeSim = float(comp[3])

    if self.frame_type == self.TypeCamera:
      self.position_x = float(comp[4])
      self.position_y = float(comp[5])
      self.position_z = float(comp[6])
      self.rotation_x = float(comp[7])
      self.rotation_y = float(comp[8])
      self.rotation_z = float(comp[9])
      self.rotation_w = float(comp[10])
      self.scale = float(comp[11])
      self.rotation_following = comp[12] == 'F'
      self.focus_node = ' '.join(comp[13:])

    elif self.frame_type == self.TypeScript:
      self.script = ' '.join(comp[4:])

    else:
      print('Unknown type in line {}'.format(line))

  def to_line(self):
    if self.frame_type == self.TypeCamera:
      if self.rotation_following:
        follow_string = 'F'
      else:
        follow_string = '-'

      return 'camera {} {} {} {} {} {} {} {} {} {} {} {} {}'.format(
        self.timeOs, self.timeRec, self.timeSim,
        self.position_x, self.position_y, self.position_z,
        self.rotation_x, self.rotation_y, self.rotation_z, self.rotation_w,
        self.scale, follow_string, self.focus_node)

    elif self.frame_type == self.TypeScript:
      return 'script {} {} {} {}'.format(self.timeOs, self.timeRec, self.timeSim, self.script)

    else:
      return 'Unknown frame type "{}"'.format(self.frame_type)
      sys.exit(1)

  def __repr__(self):
    return self.to_line(True)

def read_frames(file, cut_start, cut_end):
  with open(file) as f:
    lines = f.read().split('\n')
    header = lines[0]
    lines = lines[1:]
    # Filter empty lines
    lines = list(filter(None, lines))

    tmp_frames = []
    for line in lines:
      unwanted_scripts = [
        "1 return openspace.sessionRecording.stopRecording()",
        "1 openspace.setPropertyValueSingle('NavigationHandler.OrbitalNavigator.Friction.RotationalFriction', not openspace.getPropertyValue('NavigationHandler.OrbitalNavigator.Friction.RotationalFriction'));",
        "1 openspace.setPropertyValueSingle('NavigationHandler.OrbitalNavigator.Friction.RollFriction', not openspace.getPropertyValue('NavigationHandler.OrbitalNavigator.Friction.RollFriction'));",
        "1 openspace.setPropertyValueSingle('NavigationHandler.OrbitalNavigator.Friction.ZoomFriction', not openspace.getPropertyValue('NavigationHandler.OrbitalNavigator.Friction.ZoomFriction'));",
      ]

      f = Frame(line)

      # We don't want the commands in here that stop a recording
      if f.frame_type == Frame.TypeScript and f.script in unwanted_scripts:
        continue

      tmp_frames.append(f)

    # Renormalize recording time to 0
    first_rec_time = tmp_frames[0].timeRec
    for frame in tmp_frames:
      frame.timeRec = frame.timeRec - first_rec_time

    # -1 because of the separating frame
    last_rec_time = tmp_frames[-1].timeRec
    frames = []
    for frame in tmp_frames:
      if frame.timeRec < last_rec_time - cut_end:
        frames.append(frame)
    return header, frames

class FileInfo:
  def __init__(self, file, cut_start, cut_end, post_scripts):
    self.file = file    # Filename of the recording
    self.cut_start = cut_start  # How many seconds should be cut from the beginning
    self.cut_end = cut_end  # How many seconds should be cut from the end
    self.post_scripts = post_scripts # List of scripts that are executed after this file


# Default:
#  openspace.time.setPause(false);openspace.time.setDeltaTime(1)
files = [
  FileInfo(
    '0-introduction',
    0,
    0,
    [
      'openspace.time.setDeltaTime(1)',
       'openspace.setPropertyValueSingle("Scene.ISS_trail.Renderable.Enabled", true)'
    ]
  ),
  FileInfo(
    '1-earth',
    0,
    0,
    [
      'openspace.time.setPause(true);openspace.time.setDeltaTime(1)',
      'openspace.setPropertyValueSingle("Scene.visual.Renderable.Enabled", false)',
      'openspace.setPropertyValueSingle("Scene.gps-ops.Renderable.Enabled", false)'
      'openspace.setPropertyValueSingle("Scene.geo.Renderable.Enabled", false)',
      'openspace.setPropertyValueSingle("Scene.ISS_trail.Renderable.Enabled", false)'
    ]
  ),
  FileInfo(
    '2-apollo8launch',
    0,
    0,
    [
      'openspace.time.setPause(true); openspace.time.setDeltaTime(1)',
      'openspace.time.setTime("1968 DEC 24 16:37:31")',
      'openspace.navigation.setNavigationState({ Anchor="Apollo8",Pitch=0.568691E-4,Position={5.708252E0,1.235944E1,-1.592784E1},ReferenceFrame="Root",Up={0.960592E0,-0.212047E0,0.179718E0},Yaw=0.350570E-5 })',
      'openspace.setPropertyValue("*Trail.Renderable.Enabled", false)'
    ]
  ),
  FileInfo('3-earthrise', 0, 0, [
    'openspace.time.setPause(false);openspace.time.setDeltaTime(1)'
  ]),
  FileInfo('4-earthrise-flyout', 0, 0, [
    'openspace.time.setPause(true);openspace.time.setDeltaTime(1)'
  ]),
  FileInfo('5-apollo17-flyin', 0, 0, [
    'openspace.time.setPause(true);openspace.time.setDeltaTime(1)'
  ]),
  FileInfo('6-apollo17', 0, 0, [
    'openspace.time.setPause(true);openspace.time.setDeltaTime(1)'
  ]),
  FileInfo('7-apollo17-station6', 0, 0, [
    'openspace.time.setPause(true);openspace.time.setDeltaTime(1)',
  ]),
  FileInfo('8-moon-to-solar-system', 0, 5, [
    'openspace.time.setPause(true);openspace.time.setDeltaTime(1)'
  ]),
  FileInfo('9-solar-system-to-mars', 0, 0, [
    'openspace.time.setPause(true);openspace.time.setDeltaTime(1)'
  ]),
  FileInfo('10-solar-system', 0, 0, [
    'openspace.time.setPause(true);openspace.time.setDeltaTime(1)'
  ]),
  FileInfo('11-travel-out', 0, 0, [
    'openspace.time.setPause(true);openspace.time.setDeltaTime(1)',
    'openspace.setPropertyValueSingle("Scene.Pioneer10.Renderable.Enabled", false)',
    'openspace.setPropertyValueSingle("Scene.Pioneer11.Renderable.Enabled", false)',
    'openspace.setPropertyValueSingle("Scene.Voyager1.Renderable.Enabled", false)',
    'openspace.setPropertyValueSingle("Scene.Voyager2.Renderable.Enabled", false)'
  ]),
  FileInfo('12-travel-out-more', 0, 0, [
    'openspace.time.setPause(true);openspace.time.setDeltaTime(1)'
  ]),
  FileInfo('13-flyback', 0, 0, [
    'openspace.time.setPause(true);openspace.time.setDeltaTime(1)'
  ]),
]

all_header = ''
all_frames = []
times = []
reference_rec_time = 0
for f in files:
  header, frames = read_frames(f.file, f.cut_start, f.cut_end)
  times.append(f.file)

  if all_header == '':
    all_header = header

  if header != all_header:
    print('Different header information found: {} != {}'.format(all_header, header))
    sys.exit(1)

  for frame in frames:
    frame.timeRec = frame.timeRec + reference_rec_time

  reference_rec_time = frames[-1].timeRec
  times.append(str(reference_rec_time))
  all_frames.extend(frames)

  if len(f.post_scripts) > 0:
    frame = Frame('')
    frame.frame_type = Frame.TypeScript
    frame.timeOs = frames[-1].timeOs
    frame.timeRec = frames[-1].timeRec
    frame.timeSim = frames[-1].timeSim
    frame.script = '1 ' + ';'.join(f.post_scripts)
    all_frames.append(frame)


with open('kosmos-full', 'w') as f:
  f.write(all_header + '\n')
  for frame in all_frames:
    l = frame.to_line()
    if l != '':
      f.write(l + '\n')
  f.write('\n')

with open('kosmos-full-annotated', 'w') as f:
  for t in times:
    f.write(t + '\n')
