from django.core.exceptions import ValidationError

def validate_file_extension(value):
    valid_extensions = ['.pdf', '.jpg', '.jpeg', '.png']
    if not any(value.name.lower().endswith(ext) for ext in valid_extensions):
        raise ValidationError("Faqat PDF, JPG va PNG formatidagi fayllarni yuklashingiz mumkin!")