import datetime

from django.db.models import Q
import graphene
from graphene_django.types import DjangoObjectType

from todo.models import Todo


class TodoType(DjangoObjectType):
    class Meta:
        model = Todo


class EditTodoMutation(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        text = graphene.String()
        priority = graphene.String()
        dueDate = graphene.String()
        completed = graphene.Boolean()

    todo = graphene.Field(TodoType)

    def mutate(self, info, id, text=None, priority=None, dueDate=None, completed=False):
        todo = Todo.objects.get(pk=id)
        if text is not None:
            todo.text = text
        if priority:
            todo.priority = priority
        if dueDate:
            todo.due_date = datetime.datetime.fromisoformat(dueDate)
        todo.completed = completed
        todo.save()
        return EditTodoMutation(todo=todo)


class AddTodoInput(graphene.InputObjectType):
    # all fields are optional
    text = graphene.String()
    priority = graphene.String()
    dueDate = graphene.String()
    completed = graphene.Boolean()


class AddTodoMutation(graphene.Mutation):
    class Arguments:
        todo = AddTodoInput(required=True)

    todo = graphene.Field(TodoType)

    def mutate(self, info, todo):
        due_date = None
        completed = False
        if todo.dueDate:
            due_date = datetime.datetime.fromisoformat(todo.dueDate)
        if todo.completed is True:
            completed = True
        new_todo = Todo.objects.create(
            text=todo.text,
            priority=todo.priority or "LOW",
            due_date=due_date,
            completed=completed
        )
        return AddTodoMutation(todo=new_todo)


class DeleteTodoMutation(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, **kwargs):
        todo = Todo.objects.filter(pk=kwargs.get("id")).first()
        count, _ = todo.delete()
        deleted = True if count == 1 else False
        return DeleteTodoMutation(ok=deleted)


class Mutation(graphene.ObjectType):
    edit_todo = EditTodoMutation.Field()
    add_todo = AddTodoMutation.Field()
    delete_todo = DeleteTodoMutation.Field()


class Query(object):
    all_todos = graphene.List(TodoType)
    todo = graphene.Field(
        TodoType,
        id=graphene.String(),
        text=graphene.String()
    )

    @staticmethod
    def _get_text_filter(value) -> Q:
        if value:
            return Q(text__istartswith=value)
        return Q()

    @staticmethod
    def _get_priority_filter(value) -> Q:
        if value:
            return Q(priority=value)
        return Q()

    @staticmethod
    def _get_completed_filter(value) -> Q:
        if value is not None:
            return Q(completed=value)
        return Q()

    def resolve_all_todos(self, info, **kwargs):
        main_filter = Query._get_text_filter(kwargs.get("text")) & \
                      Query._get_priority_filter(kwargs.get("priority")) & \
                      Query._get_completed_filter(kwargs.get("completed"))

        return Todo.objects.filter(main_filter)

    def resolve_todo(self, info, **kwargs):
        _id = kwargs.get("id")
        _text = kwargs.get("text")

        if _id:
            return Todo.objects.get(id=_id)
        if _text:
            return Todo.objects.get(text=_text)
        return None
