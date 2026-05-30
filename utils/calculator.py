class SafeCalculator:
    @staticmethod
    def safe_convert_to_float(value, default=0.0):
        """Безопасно преобразует значение в float"""
        if value is None or value == '':
            return default
        try:
            return float(value)
        except (ValueError, TypeError):
            raise ValueError(f'Невозможно преобразовать "{value}" в число')

    @staticmethod
    def multiply(a, b):
        a = SafeCalculator.safe_convert_to_float(a)
        b = SafeCalculator.safe_convert_to_float(b)
        return round(a * b, 2)  # Округляем до копеек
