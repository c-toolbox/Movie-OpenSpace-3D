# V1
 - ISS near clipping
 - Near earth asteroids deltatime problem when starting up and turning down
 - Asteroid trails visible at earths limb even if transparent
 - Problems with time interpolation (due to framerate in recording?)
 - Counting Apollo 8 trails is off
 - Hard shading on the Apollo 8 module (white lines at bottom part)
 - Transition of earthrise image low fps
 - Earth blurrry and not as bright when comparing to Earthrise image
 - Apollo insignias low res?
 - Apollo trav map transition not visible / fades in immediately (needs to be loaded before, or fade is eaten up by waiting for loading)
 - Switch of heightmap on mars is visible 
 - Fade-in of asteroids strange
 - Check delta time of asteroids (time switch happens too fast)
 - Voyager pioneer lines show up too fast (delta time)
 - Constellation fade in
 - Constellation art fade in
 - Constellation lines don’t fade out
 - Exoplanet fade in
 - Jump after exoplanets
 - Milky Way black line in volume rendering in fisheye
 - Old milky way fade in when zooming out
 - Sloan introduction is too early; Sloan itself is correct
 - Planck CMB polar pinching
 - Maud’s music should be a bit later
 - Mauds music a bit louder? At least the quiet parts
 - Old milky way is visible when flying in
 - Earth jumps when going closer (follow distance node)
 - Forward rotation when flying back through Tully
 - Less reverb in audio
 - Music a bit louder compared to voice
 - Apollo 8 counting is off

# V2
## Fixes
 - Tilt a bit too high
 - ISS trail off 500 ms earlier
 - Maybe follow camera mode value wrong? (Maybe too high)
 - Zoom out to GPS Jumps position
 - Earthrise image too high up
 - Small jump after jump out from Apollo 8
 - Apollo 17 landing is in wrong location
 - Apollo 17 height map is disabled
 - Apollo 17 images too high up
 - Station 6 image not full resolution
 - Mars should have maximum level of detail
 - Asteroids have to be disabled directly after fade out
 - Milkyway volune downscaling factor too low
 - Quasars were not disabled
 - Quasars should be a bit more transparent (maybe scale a bit lower)

OpenSpace general needs a distance based map switching; not level based
Deltatime interpolation doesn’t work if the framerate is low?
Maybe need interpolation over X frames, not time; or modify based on frame rate


Introductory part: 1:36
