
def get_code(model_name, prefix="MB",size=6):
    obj = model_name.objects.last()
    prev_id = 0 if obj is None else obj.id
    current_id = int(prev_id) + 1
    return f"{prefix}{str(current_id).zfill(size)}"
