# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import bpy
import asyncio

# that's where magic happens; copied from Blender Cloud plugin
from . import async_loop

# This file shows 4 examples of operators that move the 3d cursor to scene center: 
# one syncronous for reference purposes, other three do the same thing asynchronously
# Test_OT_Async and Test_OT_NoBlock do the same thing, different approach

class Test_OT_Operator(bpy.types.Operator):
    bl_idname = "view3d.sample_1"
    bl_label = "Synchronous operator that acts immediatly"
    bl_description = "Center 3d cursor immediately"

    def execute(self, context):
        bpy.ops.view3D.snap_cursor_to_center()
        return {'FINISHED'}

class Test_OT_Mixin(bpy.types.Operator, async_loop.AsyncModalOperatorMixin):
    bl_idname = "view3d.sample_2"
    bl_label = "Asynchronous operator using AsyncModalOperatorMixin"
    bl_description = "Center 3d cursor after 3s"

    async def async_execute(self, context):
        await asyncio.sleep(3)
        bpy.ops.view3D.snap_cursor_to_center()
        self.quit()

class Test_OT_Block(bpy.types.Operator):
    bl_idname = "view3d.sample_3"
    bl_label = "Asynchronous _blocking_ operator as suggested in blender_cloud readme"
    bl_description = "Center 3d cursor after 3s"

    async def act(self):
        await asyncio.sleep(3)
        bpy.ops.view3D.snap_cursor_to_center()

    def execute(self, context):
        loop = asyncio.get_event_loop()
        res = loop.run_until_complete(self.act())
        return {'FINISHED'}

class Test_OT_NoBlock(bpy.types.Operator):
    bl_idname = "view3d.sample_4"
    bl_label = "Asynchronous non-blocking operator as suggested in blender_cloud readme"
    bl_description = "Center 3d cursor after 3s"

    async def act(self):
        await asyncio.sleep(3)
        bpy.ops.view3D.snap_cursor_to_center()

    def execute(self, context):
        async_task = asyncio.ensure_future(self.act())
        ## It's also possible to handle the task when it's done like so:
        #async_task.add_done_callback(done_callback)
        async_loop.ensure_async_loop()
        return {'FINISHED'}