from django.contrib.auth.tokens import PasswordResetTokenGenerator


class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp: int) -> str:  # noqa: ANN001
        return (
            str(user.pk)
            + str(timestamp)
            + str(user.is_active)
        )


email_verification_token = EmailVerificationTokenGenerator()
