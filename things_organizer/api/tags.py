"""

API end point for the things categories.

"""
import flask_login

from flask import jsonify
from flask_restful import Resource, abort

import things_organizer
from things_organizer import utils


class TagsAPI(Resource):
    """
    Class wrapper for the flask_restful.Resource in order to create the API.

    **NOTE:** By now the only method allow is `GET`, probably more methods will be added.

    """

    @staticmethod
    @flask_login.login_required
    def get(int_id=None):
        """
        Find a tag for a given ID, if no ID is provided it will return all available
        tags on table.

        Args:
            int_id: Id of the tag to be searched.

        Returns:
            Response from jsonify function of flask.

        """
        dict_convert = {"data": 0}
        dict_inner = {}
        lst_values = []

        if int_id is not None:
            lst_values = things_organizer.db_models.Tag.query.filter_by(id=int_id).first()

        elif int_id is None:
            lst_values = things_organizer.db_models.Tag.query.all()

        try:
            if lst_values:

                if isinstance(lst_values, list):

                    for int_inner, value in enumerate(lst_values):
                        dict_inner[int_inner] = {'id': value.id,
                                                 'name': value.name}

                    dict_convert['tags'] = dict_inner
                    dict_convert['data'] = len(lst_values)
                else:
                    dict_convert['id'] = lst_values.id
                    dict_convert['name'] = lst_values.name
                    dict_convert['data'] = 1

            else:
                dict_convert['data'] = "None"

            return jsonify(str(dict_convert))

        except Exception as excerror:
            utils.debug("Error occurred on Tags API.\nError: {}".format(excerror.__str__()))
            abort(404, error_message="Not found tag '{}'.".format(int_id))
