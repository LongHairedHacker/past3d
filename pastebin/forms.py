import re
import os
import struct

from django.forms import ModelForm
from django import forms

from pastebin.models import Geometry

facet_pattern = re.compile(r'facet normal\s+[0-9.e+-]+\s+[0-9.e+-]+\s+[0-9.e+-]+')
loop_pattern = re.compile(r'outer\s+loop')
vertex_pattern = re.compile(r'vertex\s+[0-9.e+-]+\s+[0-9.e+-]+\s+[0-9.e+-]+')
endloop_pattern = re.compile(r'endloop')
endfacet_pattern = re.compile(r'endfacet')
endsolid_pattern = re.compile(r'endsolid .*')


class STLUploadForm(ModelForm):

    def clean_file(self):

        stlfile = self.cleaned_data.get("file")
        stlfile.open()

        if stlfile.read(5) != "solid":
            #print "binary"
            #Skip header
            stlfile.seek(80)
            count = struct.unpack("i", stlfile.read(4))[0]
            if stlfile.size - 84 != count * 50:
                raise forms.ValidationError("Not a valid binary STL file.")

        else:
            #print "ascii"
            next_patterns = [facet_pattern]
            stlfile.readline()
            line = stlfile.readline().strip()

            matched_pattern = None
            vertex_count = 0

            while line != "":

                corret = False
                for pattern in next_patterns:
                    if pattern.match(line) != None:
                        corret = True
                        matched_pattern = pattern
                if not corret:
                    raise forms.ValidationError("Not a valid ascii STL file.")

                if matched_pattern == facet_pattern:
                    next_patterns = [loop_pattern]
                if matched_pattern == loop_pattern:
                    vertex_count = 0
                    next_patterns = [vertex_pattern]
                if matched_pattern == vertex_pattern:
                    vertex_count += 1
                    if vertex_count < 3:
                        next_patterns = [vertex_pattern, endloop_pattern]
                    else:
                        next_patterns = [endloop_pattern]
                if matched_pattern == endloop_pattern:
                    next_patterns = [endfacet_pattern]
                if matched_pattern == endfacet_pattern:
                    next_patterns = [facet_pattern, endsolid_pattern]

                line = stlfile.readline().strip()

            if matched_pattern != endsolid_pattern:
                raise forms.ValidationError("Not a valid ascii STL file.")

        # see https://code.djangoproject.com/ticket/20020
        # stlfile.close()
        return stlfile


class GeometryForm(STLUploadForm):

    class Meta:
        model = Geometry
        fields = ['name', 'description', 'public', 'expiration', 'file', 'sourcefile']


class AnonymousGeometryForm(STLUploadForm):
    expiration = forms.ChoiceField(choices=Geometry.EXPIRATION_CHOICES[:-1])

    class Meta:
        model = Geometry
        fields = ['name', 'description', 'public', 'expiration', 'file']
