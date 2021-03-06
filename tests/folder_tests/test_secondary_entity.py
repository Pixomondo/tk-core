# Copyright (c) 2013 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

import os
import unittest
import shutil
from mock import Mock
import tank
from tank_vendor import yaml
from tank import TankError
from tank import hook
from tank import path_cache
from tank import folder
from tank_test.tank_test_base import *


def assert_paths_to_create(expected_paths):
    """
    No file system operations are performed.
    """
    # Check paths sent to make_folder
    for expected_path in expected_paths:
        if expected_path not in g_paths_created:
            assert False, "\n%s\nnot found in: [\n%s]" % (expected_path, "\n".join(g_paths_created))
    for actual_path in g_paths_created:
        if actual_path not in expected_paths:
            assert False, "Unexpected path slated for creation: %s \nPaths: %s" % (actual_path, "\n".join(g_paths_created))


g_paths_created = []

def execute_folder_creation_proxy(self):
    """
    Proxy stub for folder creation tests
    """
    
    # now handle the path cache
    if not self._preview_mode: 
        for i in self._items:
            if i.get("action") == "entity_folder":
                path = i.get("path")
                entity_type = i.get("entity").get("type")
                entity_id = i.get("entity").get("id")
                entity_name = i.get("entity").get("name")
                self._path_cache.add_mapping(entity_type, entity_id, entity_name, path)
        for i in self._secondary_cache_entries:
            path = i.get("path")
            entity_type = i.get("entity").get("type")
            entity_id = i.get("entity").get("id")
            entity_name = i.get("entity").get("name")
            self._path_cache.add_mapping(entity_type, entity_id, entity_name, path, False)


    # finally, build a list of all paths calculated
    folders = list()
    for i in self._items:
        action = i.get("action")
        if action in ["entity_folder", "create_file", "folder"]:
            folders.append( i["path"] )
        elif action == "copy":
            folders.append( i["target_path"] )
    
    global g_paths_created
    g_paths_created = folders
    
    return folders




# test secondary entities.

class TestSchemaCreateFoldersSecondaryEntity(TankTestBase):
    def setUp(self):
        """Sets up entities in mocked shotgun database and creates Mock objects
        to pass in as callbacks to Schema.create_folders. The mock objects are
        then queried to see what paths the code attempted to create.
        """
        super(TestSchemaCreateFoldersSecondaryEntity, self).setUp()
        self.setup_fixtures("secondary_entity")
        self.seq = {"type": "Sequence",
                    "id": 2,
                    "code": "seq_code",
                    "project": self.project}
        self.shot = {"type": "Shot",
                     "id": 1,
                     "code": "shot_code",
                     "sg_sequence": self.seq,
                     # DODGY - remove when we replace the crappy sg test mocker with mockgun
                     "sg_sequence.Sequence.code": self.seq["code"],
                     "project": self.project}
        self.step = {"type": "Step",
                     "id": 3,
                     "code": "step_code",
                     "short_name": "step_short_name"}

        self.step2 = {"type": "Step",
                     "id": 33,
                     "code": "step_code_2",
                     "short_name": "step_short_name_2"}
        
        self.asset = {"type": "Asset",
                    "id": 4,
                    "sg_asset_type": "assettype",
                    "code": "assetname",
                    "project": self.project}
        
        self.task = {"type": "Task",
                     "id": 23,
                     "entity": self.shot,
                     "step": self.step,
                     # DODGY - remove when we replace the crappy sg test mocker with mockgun
                     "step.Step.short_name": self.step["short_name"],
                     "content": "task1",
                     "project": self.project}

        self.task2 = {"type": "Task",
                     "id": 25,
                     "entity": self.shot,
                     "step": self.step2,
                     # DODGY - remove when we replace the crappy sg test mocker with mockgun
                     "step.Step.short_name": self.step2["short_name"],
                     "content": "task2",
                     "project": self.project}

        entities = [self.shot, 
                    self.seq, 
                    self.step,
                    self.step2, 
                    self.project, 
                    self.asset, 
                    self.task,
                    self.task2]

        # Add these to mocked shotgun
        self.add_to_sg_mock_db(entities)

        self.tk = tank.Tank(self.project_root)

        # add mock schema data so that a list of the asset type enum values can be returned
        data = {}
        data["properties"] = {}
        data["properties"]["valid_values"] = {}
        data["properties"]["valid_values"]["value"] = ["assettype"]
        data["data_type"] = {}
        data["data_type"]["value"] = "list"        
        self.add_to_sg_schema_db("Asset", "sg_asset_type", data)

        self.schema_location = os.path.join(self.project_root, "tank", "config", "core", "schema")

        self.FolderIOReceiverBackup = folder.folder_io.FolderIOReceiver.execute_folder_creation
        folder.folder_io.FolderIOReceiver.execute_folder_creation = execute_folder_creation_proxy

    def tearDown(self):
        
        folder.folder_io.FolderIOReceiver.execute_folder_creation = self.FolderIOReceiverBackup


    def test_shot(self):
        """Tests paths used in making a shot are as expected."""
        
        expected_paths = []
        shot_path = os.path.join(self.project_root, "%s_%s" % (self.shot["code"], self.seq["code"]))
        expected_paths.extend( [self.project_root, shot_path] )

        folder.process_filesystem_structure(self.tk, 
                                            self.shot["type"], 
                                            self.shot["id"], 
                                            preview=False,
                                            engine=None)        
        
        assert_paths_to_create(expected_paths)

        # now check the path cache!
        # there shouldbe two entries, one for the shot and one for the seq        
        pc = path_cache.PathCache(self.pipeline_configuration)
        shot_paths = pc.get_paths("Shot", self.shot["id"], primary_only=False)
        seq_paths = pc.get_paths("Sequence", self.seq["id"], primary_only=False)
        self.assertEquals( len(shot_paths), 1 )
        self.assertEquals( len(seq_paths), 1)
        pc.close()
        
        # it's the same folder for seq and shot
        self.assertEquals(shot_paths, seq_paths)


    def test_task_a(self):
        """Tests paths used in making a shot are as expected."""

        folder.process_filesystem_structure(self.tk, 
                                            self.task["type"], 
                                            self.task ["id"], 
                                            preview=False,
                                            engine=None)        
        
        expected_paths = []

        shot_path = os.path.join(self.project_root, "%s_%s" % (self.shot["code"], self.seq["code"]))
        step_path = os.path.join(shot_path, "%s_%s" % (self.task["content"], self.step["short_name"]) )
        expected_paths.extend( [self.project_root, shot_path, step_path] )
        
        # add non-entity paths
        expected_paths.append(os.path.join(step_path, "images"))

        assert_paths_to_create(expected_paths)
                                
        # now check the path cache!
        # there should be two entries, one for the task and one for the step
        
        pc = path_cache.PathCache(self.pipeline_configuration)
        step_paths = pc.get_paths("Step", self.step["id"], primary_only=False)
        task_paths = pc.get_paths("Task", self.task["id"], primary_only=False)        
        self.assertEquals( len(step_paths), 1 )
        self.assertEquals( len(task_paths), 1)
        # it's the same folder for seq and shot
        self.assertEquals(step_paths, task_paths)
        pc.close()

        
        # finally check the context.
        ctx = self.tk.context_from_path(step_path)
        self.assertEquals(ctx.task["id"], self.task["id"])
        self.assertEquals(ctx.task["type"], self.task["type"])
        # now because of the double entity matching, we should have a step and a task!
        self.assertEquals(ctx.step["id"], self.step["id"])
        self.assertEquals(ctx.step["type"], self.step["type"])
                                

