"""
Sceptre template to deploy lambda using S3 with custome Code parameters
"""
from troposphere import Template, Parameter, Ref, Output, GetAtt
from troposphere.awslambda import Function, Code, Environment


class SceptreResource(object):
    def __init__(self, sceptre_user_data):
        self.sceptre_user_data = sceptre_user_data
        self.template = Template()
        self.build_function()

    def build_function(self):
        name = self.template.add_parameter(Parameter("Name", Type="String"))
        role = self.template.add_parameter(Parameter("Role", Type="String"))

        kwargs = self.sceptre_user_data
        kwargs["FunctionName"] = Ref(name)
        kwargs["Role"] = Ref(role)
        kwargs["Code"] = Code(
            S3Bucket=kwargs.pop("S3_Bucket"),
            S3Key=kwargs.pop("S3_Key"),
            S3ObjectVersion=kwargs.pop("S3_Version"),
        )

        function = self.template.add_resource(Function("Function", **kwargs))

        self.template.add_output(Output("Arn", Value=GetAtt(function, "Arn")))


def sceptre_handler(sceptre_user_data):
    return SceptreResource(sceptre_user_data).template.to_json()
