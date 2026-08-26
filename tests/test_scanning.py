import pytest
from django.urls import reverse


EICAR = b"X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"


@pytest.mark.django_db
class TestScanReport:
    def test_malicious_file_still_downloadable(self, api_client, user):
        from django.core.files.uploadedfile import SimpleUploadedFile

        api_client.force_authenticate(user=user)
        f = SimpleUploadedFile("eicar.com", EICAR)
        upload = api_client.post(reverse("file-upload"), {"file": f}, format="multipart")
        assert upload.status_code == 201
        assert upload.data["status"] == "clean"

        file_id = upload.data["id"]
        download = api_client.get(reverse("file-download", kwargs={"file_id": file_id}))
        assert download.status_code == 200

        report = api_client.get(reverse("file-report", kwargs={"file_id": file_id}))
        assert report.status_code == 200
        assert "Malicious" in report.data["summary"]
