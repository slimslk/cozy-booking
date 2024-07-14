from apps.errors.common_errors import NoContentFoundError
from apps.listings.models import Address


class AddressRepository:

    def get_address_by_id(self, address_id: int) -> Address:
        return self.get_address(pk=address_id)

    def create_address(self, address_data) -> Address:
        address = Address.objects.create(**address_data)
        return address

    def delete_address_by_id(self, address_id: int):
        address = Address.objects.filter(pk=address_id).first()
        if not address:
            raise NoContentFoundError()

    def update_address(self, address: Address) -> Address:
        address.save()
        return address

    def get_address(self, *args, **kwargs) -> Address:
        address = Address.objects.filter(**kwargs).first()
        return address
