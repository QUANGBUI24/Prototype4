from UML_MVC import uml_command_pattern as Command
from UML_ENUM_CLASS.uml_enum import InterfaceOptions as CommandType

class CommandFactory:
    def __init__(self, uml_model, view=None, class_box=None, is_gui=False):
        self.uml_model = uml_model
        self.view = view
        self.class_box = class_box
        self.is_gui = is_gui

    def create_command(self, command_name: str, class_name=None, input_name=None,
                        old_x=None, old_y=None, new_x=None, new_y=None, new_name=None,
                        old_name=None, field_type=None, method_type=None,
                        method_num=None, param_type=None,selected_param_index=None,
                        new_param_list_obj=None, new_param_list_str=None, 
                        source_class=None, dest_class=None,
                        rel_type=None, new_type=None, arrow_line=None
                    ) -> Command:

        if command_name == CommandType.MOVE_UNIT.value:
            return Command.MoveUnitCommand(
                class_box=self.class_box,
                old_x=old_x, 
                old_y=old_y, 
                new_x=new_x, 
                new_y=new_y
            )
        elif command_name == CommandType.ADD_CLASS.value:
            return Command.AddClassCommand(
                class_name=class_name,
                uml_model=self.uml_model,
                view=self.view,
                class_box=self.class_box,
                is_gui=self.is_gui,
            )
        elif command_name == CommandType.DELETE_CLASS.value:
            return Command.DeleteClassCommand(
                class_name=class_name,
                uml_model=self.uml_model,
                view=self.view,
                class_box=self.class_box,
                is_gui=self.is_gui,
            )
        elif command_name == CommandType.RENAME_CLASS.value:
            return Command.RenameClassCommand(
                class_name=class_name,
                new_name=new_name,
                uml_model=self.uml_model,
                view=self.view,
                class_box=self.class_box,
                is_gui=self.is_gui,
            )
        elif command_name == CommandType.ADD_FIELD.value:
            return Command.AddFieldCommand(
                class_name=class_name,
                type=field_type,
                field_name=input_name,
                uml_model=self.uml_model,
                view=self.view,
                class_box=self.class_box,
                is_gui=self.is_gui,
            )
        elif command_name == CommandType.DELETE_FIELD.value:
            return Command.DeleteFieldCommand(
                class_name=class_name,
                field_name=input_name,
                uml_model=self.uml_model,
                view=self.view,
                class_box=self.class_box,
                is_gui=self.is_gui,
            )
        elif command_name == CommandType.RENAME_FIELD.value:
            return Command.RenameFieldCommand(
                class_name=class_name,
                old_field_name=old_name,
                new_field_name=new_name,
                uml_model=self.uml_model,
                view=self.view,
                class_box=self.class_box,
                is_gui=self.is_gui,
            )
        elif command_name == CommandType.ADD_METHOD.value:
            return Command.AddMethodCommand(
                class_name=class_name,
                type=method_type,
                method_name=input_name,
                uml_model=self.uml_model,
                view=self.view,
                class_box=self.class_box,
                is_gui=self.is_gui,
            )
        elif command_name == CommandType.DELETE_METHOD.value:
            return Command.DeleteMethodCommand(
                class_name=class_name,
                method_num=method_num,
                uml_model=self.uml_model,
                view=self.view,
                class_box=self.class_box,
                is_gui=self.is_gui,
            )
        elif command_name == CommandType.RENAME_METHOD.value:
            return Command.RenameMethodCommand(
                class_name=class_name,
                method_num=method_num,
                new_name=new_name,
                uml_model=self.uml_model,
                view=self.view,
                class_box=self.class_box,
                is_gui=self.is_gui,
            )
        elif command_name == CommandType.ADD_PARAM.value:
            return Command.AddParameterCommand(
                class_name=class_name,
                method_num=method_num,
                param_type=param_type,
                param_name=input_name,
                uml_model=self.uml_model,
                view=self.view,
                class_box=self.class_box,
                is_gui=self.is_gui,
            )
        elif command_name == CommandType.DELETE_PARAM.value:
            return Command.DeleteParameterCommand(
                class_name=class_name,
                method_num=method_num,
                selected_param_index=selected_param_index,
                param_name=input_name,
                uml_model=self.uml_model,
                view=self.view,
                class_box=self.class_box,
                is_gui=self.is_gui,
            )
        elif command_name == CommandType.RENAME_PARAM.value:
            return Command.RenameParameterCommand(
                class_name=class_name,
                method_num=method_num,
                old_param_name=old_name,
                new_param_name=new_name,
                uml_model=self.uml_model,
                view=self.view,
                class_box=self.class_box,
                is_gui=self.is_gui,
            )
        elif command_name == CommandType.REPLACE_PARAM.value:
            return Command.ReplaceParameterListCommand(
                class_name=class_name,
                method_num=method_num,
                new_param_list_obj=new_param_list_obj,
                new_param_list_str=new_param_list_str,
                uml_model=self.uml_model,
                view=self.view,
                class_box=self.class_box,
                is_gui=self.is_gui,
            )
        elif command_name == CommandType.ADD_REL.value:
            return Command.AddRelationshipCommand(
                source_class=source_class,
                dest_class=dest_class,
                rel_type=rel_type,
                uml_model=self.uml_model,
                view=self.view,
                class_box=self.class_box,
                is_gui=self.is_gui,
            )
        elif command_name == CommandType.DELETE_REL.value:
            return Command.DeleteRelationshipCommand(
                source_class=source_class,
                dest_class=dest_class,
                uml_model=self.uml_model,
                view=self.view,
                class_box=self.class_box,
                is_gui=self.is_gui,
            )
        elif command_name == CommandType.EDIT_FIELD_TYPE.value:
            return Command.ChangeTypeCommand(
            class_name=class_name,
            input_name=input_name,
            new_type=new_type,
            is_field=True,
            uml_model=self.uml_model,
            view=self.view,
            class_box=self.class_box,
            is_gui=self.is_gui,
        )
        elif command_name == CommandType.EDIT_METHOD_TYPE.value:
            return Command.ChangeTypeCommand(
                class_name=class_name,
                method_num=method_num,
                new_type=new_type,
                is_method=True,
                uml_model=self.uml_model,
                view=self.view,
                class_box=self.class_box,
                is_gui=self.is_gui,
            )
        elif command_name == CommandType.EDIT_PARAM_TYPE.value:
            return Command.ChangeTypeCommand(
                class_name=class_name,
                method_num=method_num,
                input_name=input_name,
                new_type=new_type,
                is_param=True,
                uml_model=self.uml_model,
                view=self.view,
                class_box=self.class_box,
                is_gui=self.is_gui,
            )
        elif command_name == CommandType.EDIT_REL_TYPE.value:
            return Command.ChangeTypeCommand(
                source_class=source_class,
                dest_class=dest_class, 
                new_type=new_type,
                arrow_line=arrow_line,
                is_rel=True,
                uml_model=self.uml_model,
                view=self.view,
                class_box=self.class_box,
                is_gui=self.is_gui,
            )