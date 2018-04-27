#! /usr/bin/env python
'''=Instanced Geometry and Texture Buffer Extensions=

[shader_instanced.py-screen-0001.png Screenshot]

This tutorial:

    * uses an instanced geometry rendering extension to draw lots of geometry
    * introduces the use of texture buffer objects and the texelFetch GLSL 
      function
'''
from __future__ import print_function
#import OpenGL
#OpenGL.FORWARD_COMPATIBLE_ONLY = True
from shader_11 import TestContext as BaseContext
from OpenGL.GL import *
from OpenGLContext.arrays import *
from OpenGLContext.scenegraph.basenodes import *
'''ARB_draw_instanced is an extremely common extension available on most modern 
discrete OpenGL cards.  It defines a mechanism whereby you can generate a large 
number of "customized" instances of a given piece of geometry using a single call 
to the GL.  It requires the use of shaders, as the only difference between the 
calls is a shader variable:

    gl_InstanceIDARB

which is incremented by one for each instance.

The ARB_draw_instanced extension is part of core OpenGL 3.3, so the entry 
points are available from the OpenGL.GL namespace by default (for all versions 
of PyOpenGL >= 3.0.2), thus you could omit this line with a newer PyOpenGL.'''
from OpenGL.GL.ARB.draw_instanced import *
'''ARB_texture_buffer_object is also extremely common, and core as of OpenGL 3.0.
It defines a mechanism that allows you to pass large "reference" arrays into a 
shader efficiently (using a Vertex Buffer Object).  Combined with draw_instanced,
we will set up a reference array which defines the positions of each of our 
instanced objects.

Again, the import here is just for use with older PyOpenGL releases.
'''
from OpenGL.GL.ARB.texture_buffer_object import *
'''For our sample code, we'll create an array of N spheres to render.  We'll 
use the numpy module "random" to generate a few offsets.
'''
from numpy import random

class TestContext( BaseContext ):
    def OnInit( self ):
        """Initialize the context"""
        '''Our basic setup is the same as our previous tutorial...'''
        self.lights = self.createLights()
        self.LIGHTS = array([
            self.lightAsArray(l)
            for l in self.lights
        ],'f')
        self.shader_constants['LIGHT_COUNT'] = len(self.lights)
        light_preCalc = GLSLImport( url='_shader_tut_lightprecalc.vert' )
        phong_preCalc = GLSLImport( url="res://phongprecalc_vert" )
        phong_weightCalc = GLSLImport( url="res://phongweights_frag" )
        lightConst = GLSLImport( source = "\n".join([
                "const int %s = %s;"%( k,v )
                for k,v in self.shader_constants.items()
            ]) + """
            uniform vec4 lights[ LIGHT_COUNT*LIGHT_SIZE ];

            varying vec3 EC_Light_half[LIGHT_COUNT];
            varying vec3 EC_Light_location[LIGHT_COUNT];
            varying float Light_distance[LIGHT_COUNT];

            varying vec3 baseNormal;
            varying vec2 Vertex_texture_coordinate_var;
            """
        )
        '''To make the instanced geometry do something, we have to pass in a data-array 
        which will be indexed by the gl_InstanceIDARB variable.  For this simple tutorial 
        we will use an array of offsets which are applied to the geometry.  We will use 
        len(offset) values here.  We'll limit the value to less than the allowed number of 
        bytes in the texture buffer object (we divide by 16 as that's the length of a single 
        texel in float format).
        '''
        hardlimit = glGetIntegerv( GL_MAX_TEXTURE_BUFFER_SIZE_ARB )
        count = min((15000,hardlimit//16))
        print('Limiting to %s instances'%( count, ))
        '''This is just some calculations to make the 0-1 range of random.random() map into 
        values that put the bulk of the spheres in front of the camera.'''
        scale = [40,40,40,0]
        offset = [-20,-20,-40,1]
        '''We create our random data-array to serve as the positions for the 
        individual instances.  Note that there are (hardware) restrictions on the 
        formats allowed in texture_buffer_object VBOs.  The most notable of those is 
        that you *must* use 1,2 or 4 components per texel.  For three components, 
        as we need, you must either use a single-value texture with 3x the values,
        or pad the data with an extra byte.  OpenGL 4.x allows for 3-component 
        values, but we'll avoid the extra dependency for now.
        '''
        self.offset_array = (
            # we require RGBA to be compatible with < OpenGL 4.x
            random.random( size=(count,4 ) ) * scale + offset
        ).astype('f')
        '''The texture buffer extension works via a GL texture, so we bind it using 
        a TextureBufferUniform node which is analogous to a TextureUniform, save that 
        it uses a ShaderBuffer instead of an ImageTexture as its "value" member.  We 
        will create a new uniform sampler in our shader to bind this texture (unit).
        
        At render-time the TextureBufferUniform will:
        
         * lookup the uniform name "offsets_table"
         * bind the uniform to a texture unit 
         * create and bind a texture object 
         * configure the texture to use a VBO as its data source  with a given format
        '''
        TEXTURE_BUFFER_UNIFORM = TextureBufferUniform(
            name='offsets_table',
            format='RGBA32F',
            value = ShaderBuffer(
                usage = 'STATIC_DRAW',
                type = 'TEXTURE',
                buffer = self.offset_array,
            ),
        )
        '''Now our Vertex Shader, which is only a tiny change from our previous shader,
        basically it just adds offset_table[gl_InstanceIDARB] to the Vertex_position to get 
        the new position for the vertex being generated.  However, the offset_table is actually 
        a texture, so we have to go through the special sampler type samplerBuffer and 
        the direct texel retrieval function texelFetch to accomplish the lookup.
        Note the .xyz on the result of the lookup, see above for a discussion of the limitations
        on the data-formats for Texture Buffer objects.'''
        VERTEX_SHADER = """
        attribute vec3 Vertex_position;
        attribute vec3 Vertex_normal;
        attribute vec2 Vertex_texture_coordinate;
        uniform samplerBuffer offsets_table;
        void main() {
            vec3 offset = texelFetch( offsets_table, gl_InstanceIDARB ).xyz;
            vec3 final_position = Vertex_position + offset;
            gl_Position = gl_ModelViewProjectionMatrix * vec4(
                final_position, 1.0
            );
            baseNormal = gl_NormalMatrix * normalize(Vertex_normal);
            light_preCalc(final_position);
            Vertex_texture_coordinate_var = Vertex_texture_coordinate;
        }"""
        '''We set up our GLSLObjects as before, using VERTEX_SHADER as the source 
        for our GLSLShader vertex object, and using the TextureBufferUniform above .
        '''
        self.glslObject = GLSLObject(
            uniforms = [
                FloatUniform1f(name="material.shininess", value=.5 ),
                FloatUniform4f(name="material.ambient", value=(.1,.1,.1,1.0) ),
                FloatUniform4f(name="material.diffuse", value=(1.0,1.0,1.0,1.0) ),
                FloatUniform4f(name="material.specular", value=(.4,.4,.4,1.0) ),
                FloatUniform4f(name="Global_ambient", value=(.1,.1,.1,1.0) ),
                FloatUniform4f(name="lights" ),
            ],
            textures = [
                TextureUniform(name="diffuse_texture", value=ImageTexture(
                    url="marbleface.jpeg",
                )),
                TEXTURE_BUFFER_UNIFORM,
            ],
            shaders = [
                GLSLShader(
                    version = '330',
                    imports = [
                        lightConst,
                        phong_preCalc,
                        light_preCalc,
                    ],
                    source = [
                        VERTEX_SHADER
                    ],
                    type='VERTEX'
                ),
                GLSLShader(
                    imports = [
                        lightConst,
                        phong_weightCalc,
                    ],
                    source = [
                        """
                        struct Material {
                            vec4 ambient;
                            vec4 diffuse;
                            vec4 specular;
                            float shininess;
                        };
                        uniform Material material;
                        uniform vec4 Global_ambient;
                        uniform sampler2D diffuse_texture;

                        void main() {
                            vec4 fragColor = Global_ambient * material.ambient;

                            vec4 texDiffuse = texture2D(
                                diffuse_texture, Vertex_texture_coordinate_var
                            );
                            texDiffuse = mix( material.diffuse, texDiffuse, .5 );

                            // Again, we've moved the "hairy" code into the reusable
                            // function, our loop simply calls the phong calculation
                            // with the values from our uniforms and attributes...
                            int i,j;
                            for (i=0;i<LIGHT_COUNT;i++) {
                                j = i * LIGHT_SIZE;
                                vec3 weights = phong_weightCalc(
                                    normalize(EC_Light_location[i]),
                                    normalize(EC_Light_half[i]),
                                    normalize(baseNormal),
                                    material.shininess,
                                    abs(Light_distance[i]), // see note tutorial 9
                                    lights[j+ATTENUATION],
                                    lights[j+SPOT_PARAMS],
                                    lights[j+SPOT_DIR]
                                );
                                fragColor = (
                                    fragColor
                                    + (lights[j+AMBIENT] * material.ambient * weights.x)
                                    + (lights[j+DIFFUSE] * texDiffuse * weights.y)
                                    + (lights[j+SPECULAR] * material.specular * weights.z)
                                );
                            }
                            gl_FragColor = fragColor;
                        }
                        """
                    ],
                    type='FRAGMENT',
                ),
            ],
        )
        '''We tell our sphere to generate fewer "slices" in its tessellation by reducing it's "phi" 
        parameter.'''
        coords,indices = Sphere(
            radius = .25,
            phi = pi/8.0
        ).compileArrays()
        self.coords = ShaderBuffer( buffer = coords )
        self.indices = ShaderIndexBuffer( buffer = indices )
        '''For interest sake, we print out the number of objects/triangles being rendered.  Reasonably 
        capable hardware should be able to handle extremely large numbers of instances (thousands).'''
        self.count = len(indices)
        print('Each sphere has %s triangles, total of %s triangles'%( self.count//3, self.count//3 * len(self.offset_array) ))
        '''Our attribute setup is unchanged.'''
        stride = coords[0].nbytes
        self.attributes = [
            ShaderAttribute(
                name = 'Vertex_position',
                offset = 0,
                stride = stride,
                buffer = self.coords,
                isCoord = True,
            ),
            ShaderAttribute(
                name = 'Vertex_texture_coordinate',
                offset = 4*3,
                stride = stride,
                buffer = self.coords,
                size = 2,
                isCoord = False,
            ),
            ShaderAttribute(
                name = 'Vertex_normal',
                offset = 4*5,
                stride = stride,
                buffer = self.coords,
                isCoord = False,
            ),
        ]
        self.appearance = Appearance(
            material = Material(
                diffuseColor = (1,1,1),
                ambientIntensity = .1,
                shininess = .5,
            ),
        )
    
    '''The only change to our render method is in the glDrawElements call, which 
    is replaced by a call to glDrawElementsInstanced'''
    def Render( self, mode = None):
        """Render the geometry for the scene."""
        if not mode.visible:
            return
        for i,light in enumerate( self.lights ):
            self.LIGHTS[i] = self.lightAsArray( light )
        self.glslObject.getVariable( 'lights' ).value = self.LIGHTS
        for key,value in self.materialFromAppearance(
            self.appearance, mode
        ).items():
            self.glslObject.getVariable( key ).value = value
        token = self.glslObject.render( mode )
        tokens = [  ]
        try:
            vbo = self.indices.bind(mode)
            for attribute in self.attributes:
                token = attribute.render( self.glslObject, mode )
                if token:
                    tokens.append( (attribute, token) )
            '''The final parameter to glDrawElementsInstanced simply tells the 
            GL how many instances to generate.  gl_InstanceIDARB values will be 
            generated for range( instance_count ) instances.'''
            glDrawElementsInstanced(
                GL_TRIANGLES, self.count,
                GL_UNSIGNED_INT, vbo,
                len(self.offset_array), # number of instances to draw...
            )
        finally:
            for attribute,token in tokens:
                attribute.renderPost( self.glslObject, mode, token )
            self.glslObject.renderPost( token, mode )
            vbo.unbind()

if __name__ == "__main__":
    #TestContext.ContextMainLoop(debug=False,profile='core',version=(3,3))
    TestContext.ContextMainLoop()
