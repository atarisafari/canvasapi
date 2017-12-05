from __future__ import absolute_import, division, print_function, unicode_literals

from six import python_2_unicode_compatible

from canvasapi.canvas_object import CanvasObject
from canvasapi.util import combine_kwargs
from canvasapi.quiz_group import QuizGroup
from canvasapi.exceptions import RequiredFieldMissing


@python_2_unicode_compatible
class Quiz(CanvasObject):

    def __str__(self):
        return "{} ({})".format(self.title, self.id)

    def edit(self, **kwargs):
        """
        Modify this quiz.

        :calls: `PUT /api/v1/courses/:course_id/quizzes/:id \
        <https://canvas.instructure.com/doc/api/quizzes.html#method.quizzes/quizzes_api.update>`_

        :returns: The updated quiz.
        :rtype: :class:`canvasapi.quiz.Quiz`
        """
        response = self._requester.request(
            'PUT',
            'courses/{}/quizzes/{}'.format(self.course_id, self.id),
            _kwargs=combine_kwargs(**kwargs)
        )
        quiz_json = response.json()
        quiz_json.update({'course_id': self.course_id})

        return Quiz(self._requester, quiz_json)

    def delete(self, **kwargs):
        """
        Delete this quiz.

        :calls: `DELETE /api/v1/courses/:course_id/quizzes/:id \
        <https://canvas.instructure.com/doc/api/quizzes.html#method.quizzes/quizzes_api.destroy>`_

        :rtype: :class:`canvasapi.quiz.Quiz`
        """
        response = self._requester.request(
            'DELETE',
            'courses/{}/quizzes/{}'.format(self.course_id, self.id),
            _kwargs=combine_kwargs(**kwargs)
        )
        quiz_json = response.json()
        quiz_json.update({'course_id': self.course_id})

        return Quiz(self._requester, quiz_json)

    def get_quiz_group(self, id):
        """
        Get details of the quiz group with the given id

        :calls: `GET /api/v1/courses/:course_id/quizzes/:quiz_id/groups/:id \
        <https://canvas.instructure.com/doc/api/quiz_question_groups.html#method.quizzes/quiz_groups.show>`


        :param id: The ID of the question group.
        :type: `int`

        :returns: `QuizGroup` object
        :rtype: :class:`canvasapi.quiz_group.QuizGroup`
        """
        response = self._requester.request(
            'GET',
            'courses/{}/quizzes/{}/groups/{}'.format(self.course_id, self.id, id)
        )

        response_json = response.json()
        response_json.update({'course_id': self.id})

        return QuizGroup(self._requester, response_json)

    def create_question_group(self, quiz_groups, **kwargs):
        """
        Create a new question group for the given quiz id

        :calls: `POST /api/v1/courses/:course_id/quizzes/:quiz_id/groups/:id \
        <https://canvas.instructure.com/doc/api/quiz_question_groups.html#method.quizzes/quiz_groups.create>`

        :param quiz_groups: The name, pick count, question points,
        and/or assessment question bank id.
        All of these parameters are optional, but at least one must exist
        (even if empty) to recieve a response.
        The request expects a list, but will only create 1 question group per request.
        :type list[dict]

        :returns: `QuizGroup` object
        :rtype: :class:`canvasapi.quiz_group.QuizGroup`
        """

        if not isinstance(quiz_groups, list) or len(quiz_groups) <= 0:
            raise ValueError("Param `quiz_groups` must be a non-empty list.")

        if not isinstance(quiz_groups[0], dict):
            raise ValueError("Param `quiz_groups must contain a dictionary")

        if ("name" not in quiz_groups[0] and "pick_count" not in quiz_groups[0]
            and "question_points" not in quiz_groups[0]
                and "assessment_question_bank_id" not in quiz_groups[0]):
            raise RequiredFieldMissing("quiz_groups must contain at least 1 parameter.")

        kwargs["quiz_groups"] = quiz_groups

        response = self._requester.request(
            'POST',
            'courses/{}/quizzes/{}/groups'.format(self.course_id, self.id),
            _kwargs=combine_kwargs(**kwargs)
        )

        response_json = response.json()
        response_json['quiz_groups'][0].update({'course_id': self.id})

        return QuizGroup(self._requester, response_json.get('quiz_groups')[0])
