import docker as dk

class LB:
    def __init__(self):
        self.docker_client = dk.from_env()
        self._index = 0 

    @property
    def reachable_container_amount(self):
        return len(self.reachable_container_list)
    
    @property
    def reachable_container_list(self):
        return [container for container in self.docker_client.containers.list() if self._is_reachable(container)]

    def next(self):
        self._increase_index()
        print("Index:", self._index, "Containers:", self.reachable_container_amount)
        target = self._container_url(self.reachable_container_list[self._index]) 
        return target 
    
    def _container_url(self, container):
        connection_data = next(iter(container.ports.items()))[1][0]
        return f"{connection_data['HostIp']}:{connection_data['HostPort']}/"
    
    def _increase_index(self):
        self._index += 1
        if self._index >= self.reachable_container_amount:
            self._index = 0
    
    def _is_reachable(self, container):
        return bool(next(iter(container.ports.items()), [False, False])[1])