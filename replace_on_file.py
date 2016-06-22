import re
import textwrap

# Read in the file
filedata = None
with open('surf_test.pov', 'r') as file:
    filedata = file.read()

# Add a new texture to the texture declarations for every
# mesh point
filedata = filedata.replace(r'texture {', 'texture { my_texture')

# Remove initial comments
filedata = re.sub(re.compile('//.*?\n', re.DOTALL), '', filedata)

# Remove default global_settings declaration
filedata = re.sub(re.compile('global_settings\s{.*?}\n', re.DOTALL),
                  '',
                  filedata
                  )

# Remove any light sources
filedata = re.sub(re.compile('light_source\s{.*?}\n', re.DOTALL),
                  '',
                  filedata
                  )

# We add a custom preamble with better lights and
# settings for Povray
preamble_text = textwrap.dedent("""
    // Edited PovRay file from Mayavi
    // Run with: povray surf_test.pov +W2200 +H1900 +A
    #include "rad_def.inc"
    #include "colors.inc"

    // Material - phong lighting makes a kind of plastic look
    #declare my_texture = finish { phong 1 phong_size 20 ambient 0
                                   reflection{metallic 0}
                          };

    // These are tricky but should work for different scenes
    // Radiosity is important for better shadows
    global_settings {
          max_trace_level 30
          assumed_gamma 1.5
          radiosity { error_bound 1.3 //start here and decrease slowly until splotchiness disappears
                      nearest_count 10 //or higher, up to 20
                      recursion_limit 2 //should be fine for this
          }
    }

    // We will use an area light since it creates diffused shadows
    // Another possibility would be to create a spotlight

    // Light centered at <-3,-3, 4>, propagating towards the two
    // directions in area_light and 6, 6 means a 6 by 6
    // array of lights (check PovRay doc)
    // jitter creates random lights to get better shadows
    light_source { <-3, -3, 4.>
                   color White
                   area_light <6, 0, 0>, <0, 6, 0>, 6, 6
                   area_illumination on
                   jitter
                   // adaptive 1
                 }

    // Adding a plane makes the surface more realistic
    // The position will depend on the Mayavi Scene
    plane
    {
        // Plane normal vector at <0, 0, 0> and -1 is the
        // translation along this direction
        <0, 0, 1>, -1
        texture{ pigment { color rgb < 1, 1, 1 > }
                 finish{ ambient 0 diffuse 0.5 }
        }
    }

    """
)


filedata = preamble_text + filedata

# Write the file out again
with open('surf_test.pov', 'w') as file:
    file.write(filedata)
