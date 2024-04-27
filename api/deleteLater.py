from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_categories = models.ManyToManyField(Category)
    preferences_set = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


from rest_framework import serializers
from .models import UserProfile, Category


class UserProfileSerializer(serializers.ModelSerializer):
    preferred_categories = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all()
    )

    class Meta:
        model = UserProfile
        fields = ["user", "preferred_categories", "preferences_set"]

    def validate_preferred_categories(self, value):
        if not value:
            raise serializers.ValidationError("You must select at least one category.")
        return value

    def update(self, instance, validated_data):
        instance.preferred_categories.set(validated_data["preferred_categories"])
        instance.preferences_set = True
        instance.save()
        return instance


from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile
from .serializers import UserProfileSerializer
from rest_framework.response import Response


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, preferences_set=False)

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useHistory } from 'react-router-dom';

const Preferences = () => {
    const [categories, setCategories] = useState([]);
    const [selectedCategories, setSelectedCategories] = useState([]);
    const history = useHistory();

    useEffect(() => {
        axios.get('/api/categories/')
            .then(res => setCategories(res.data));
    }, []);

    const handleSelectCategory = category => {
        const newSelection = selectedCategories.includes(category)
            ? selectedCategories.filter(cat => cat !== category)
            : [...selectedCategories, category];
        setSelectedCategories(newSelection);
    };

    const handleSubmit = () => {
        axios.post('/api/userprofile/', { preferred_categories: selectedCategories })
            .then(() => history.push('/homepage'))
            .catch(error => alert('You must select at least one category.'));
    };

    return (
        <div>
            <h1>Choose Your Preferences</h1>
            {categories.map(category => (
                <button key={category.id} onClick={() => handleSelectCategory(category.id)}>
                    {category.name}
                </button>
            ))}
            <button onClick={handleSubmit}>Submit


import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Preferences = ({ history }) => {
    const [categories, setCategories] = useState([]);
    const [selectedCategories, setSelectedCategories] = useState([]);

    useEffect(() => {
        axios.get('/api/preferences/')
            .then(res => {
                if (res.data.message === 'Preferences already set.') {
                    history.push('/homepage');
                }
                setCategories(res.data.categories || []);
            })
            .catch(err => console.error(err));
    }, [history]);

    const handleCategorySelect = (category) => {
        const updatedSelection = selectedCategories.includes(category)
            ? selectedCategories.filter(c => c !== category)
            : [...selectedCategories, category];
        setSelectedCategories(updatedSelection);
    };

    const handleSubmit = () => {
        axios.post('/api/preferences/', { preferred_categories: selectedCategories })
            .then(() => history.push('/homepage'))
            .catch(err => console.error(err));
    };

    return (
        <div>
            <h1>Select Your Preferences</h1>
            <ul>
                {categories.map
