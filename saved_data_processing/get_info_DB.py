from saved_data_processing import data_formatter_DB


class GetInfo:

    def __init__(self, username, info, resources=None, resources_bbrc=None):

        self.formatter_object = data_formatter_DB.Formatter(username)
        self.info = info
        self.resources = resources
        self.resources_bbrc = resources_bbrc

    def __preprocessor(self):

        '''
        This preprocessor makes the final dictionary with each key representing
        a graph.
        In return data each key and value pair represent a graph.
        If the key and value doesn't represent a graph further processing will
        be done.
        In the current case only 4 key and value pair have this structure:
        Number of projects
        Number of subjects
        Number of experiments
        Number of scans

        Return type of this function is a single dictionary with each key and
        value pair representing graph.
        '''

        stats = {}
        final_json_dict = {}

        # Preprocessing required in project data for number of projects
        projects_details = self.formatter_object.get_projects_details(
            self.info['projects'])
        # If some error in connection 1 will be returned and we will
        # not go further
        if type(projects_details) != int:
            stats['Projects'] = projects_details['Number of Projects']
            del projects_details['Number of Projects']
        else:
            return projects_details

        # Pre processing for subject details required
        subjects_details = self.formatter_object.get_subjects_details(
            self.info['subjects'])
        if subjects_details != 1:
            stats['Subjects'] = subjects_details['Number of Subjects']
            del subjects_details['Number of Subjects']

        # Pre processing experiment details
        experiments_details = self.formatter_object.get_experiments_details(
            self.info['experiments'])

        if experiments_details != 1:
            stats['Experiments'] = experiments_details['Number of Experiments']
            del experiments_details['Number of Experiments']

        # Pre processing scans details
        scans_details = self.formatter_object.get_scans_details(
            self.info['scans'])
        if scans_details != 1:
            stats['Scans'] = scans_details['Number of Scans']
            del scans_details['Number of Scans']

        stat_final = {'Stats': stats}

        final_json_dict.update(projects_details)
        final_json_dict.update(subjects_details)
        final_json_dict.update(experiments_details)
        final_json_dict.update(scans_details)
        final_json_dict.update(stat_final)

        resources = self.formatter_object.get_resources_details(
            self.resources, self.resources_bbrc)

        if resources is not None and type(resources) != int:

            final_json_dict.update(resources)

        '''
        returns a nested dict
        {
            Graph1_name : { x_axis_values, y_axis_values},
            Graph2_name : { x_axis_values, y_axis_values},
            Graph3_name : { x_axis_values, y_axis_values},
            Graph4_name : { x_axis_values, y_axis_values},
        }
        '''

        return final_json_dict

    def get_project_list(self):

        return self.formatter_object.get_projects_details_specific(
            self.info['projects'])

    def get_info(self):

        return self.__preprocessor()


class GetInfoPP(GetInfo):

    def __init__(
            self,
            username,
            info, project_id, resources=None, resources_bbrc=None):

        self.formatter_object_per_project = data_formatter_DB.FormatterPP(
            username, project_id)
        self.info = info
        self.resources = resources
        self.username = username
        self.project_id = project_id
        self.resources_bbrc = resources_bbrc

    def __preprocessor_per_project(self):

        '''
        This preprocessor makes the final dictionary with each key representing
        a graph.
        In return data each key and value pair represent a graph.
        If the key and value doesn't represent a graph further processing will
        be done.
        In the current case only 4 key and value pair have this structure:
        Number of projects
        Number of subjects
        Number of experiments
        Number of scans

        Return type of this function is a single dictionary with each key and
        value pair representing graph.
        '''

        stats = {}
        final_json_dict = {}

        # Preprocessing required in project data for number of projects
        projects_details = self.formatter_object_per_project.\
            get_projects_details(self.info['projects'])

        # Pre processing for subject details required
        subjects_details = self.formatter_object_per_project.\
            get_subjects_details(self.info['subjects'])

        if subjects_details != 1:
            stats['Subjects'] = subjects_details['Number of Subjects']
            del subjects_details['Number of Subjects']

        # Pre processing experiment details
        experiments_details = self.formatter_object_per_project.\
            get_experiments_details(self.info['experiments'])

        if experiments_details != 1:
            stats['Experiments'] = experiments_details['Number of Experiments']
            del experiments_details['Sessions types/Project']
            del experiments_details['Number of Experiments']

        # Pre processing scans details
        scans_details = self.formatter_object_per_project.\
            get_scans_details(self.info['scans'])

        if scans_details != 1:
            stats['Scans'] = scans_details['Number of Scans']
            del scans_details['Number of Scans']

        stat_final = {'Stats': stats}

        final_json_dict.update({'Project details': projects_details})
        final_json_dict.update(subjects_details)
        final_json_dict.update(experiments_details)
        final_json_dict.update(scans_details)
        final_json_dict.update(stat_final)

        resources = self.formatter_object_per_project.get_resources_details(
            self.resources, self.resources_bbrc)

        if type(resources) != int and resources is not None:

            final_json_dict.update(resources)

        diff_dates = self.formatter_object_per_project.diff_dates(
            self.resources_bbrc, self.info['experiments'])

        if diff_dates is not None and diff_dates['count'] != {}:

            final_json_dict.update({'Dates Diff': diff_dates})

        '''
        returns a nested dict
        {
            Graph1_name : { x_axis_values, y_axis_values},
            Graph2_name : { x_axis_values, y_axis_values},
            Graph3_name : { x_axis_values, y_axis_values},
            Graph4_name : { x_axis_values, y_axis_values},
        }
        '''

        return final_json_dict

    def get_per_project_view(self):

        return self.__preprocessor_per_project()
