import pytest
import rest_framework.reverse
from rest_framework import status

from .models import Project, Task

# Create your tests here.

pytestmark = pytest.mark.django_db  # All tests use db

TEST_SIZE = 10000


@pytest.fixture
def project():
    return Project.objects.create(name='Test')


@pytest.fixture
def tasks(project):
    tasks = []
    for i in range(TEST_SIZE):
        tasks.append(Task.objects.create(project=project, name='Test_{}'.format(i)))

    return tasks


class TestTaskUpdate:
    def test_update_task(self, client, project, tasks):
        for x in range(TEST_SIZE):
            test_url = rest_framework.reverse.reverse(
                "project-task-update",
                kwargs={
                    "project_id": project.id,
                    "id": tasks[x].id
                },
            )
            # test auto setting sequence
            response = client.put(
                test_url,
                data={'name': 'Test_{0}_{0}'.format(x),
                      'description': "test",
                      }
            )

            assert response.status_code == status.HTTP_200_OK


def func(x):
    return x + 1


def test_answer():
    assert func(3) == 5
