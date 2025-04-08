class TorrentTracker {
    constructor() {
        this.trackers = [
            'udp://tracker.opentrackr.org:1337/announce',
            'udp://tracker.openbittorrent.com:6969/announce',
            // Añade más trackers según necesites
        ];
    }

    async updateStats(infoHash) {
        try {
            const response = await fetch(`/api/torrent-stats/${infoHash}`);
            if (!response.ok) throw new Error('Error fetching stats');
            
            const stats = await response.json();
            return stats;
        } catch (error) {
            console.error('Error updating torrent stats:', error);
            return null;
        }
    }

    updateTorrentDisplay(container, stats) {
        const seedsElement = container.querySelector('.seeds-count');
        const peersElement = container.querySelector('.peers-count');
        
        if (stats) {
            seedsElement.textContent = stats.seeds;
            peersElement.textContent = stats.peers;
            
            // Actualizar indicadores visuales
            this.updateHealthIndicator(container, stats);
        }
    }

    updateHealthIndicator(container, {seeds, peers}) {
        const healthStatus = this.calculateHealth(seeds, peers);
        const indicator = container.querySelector('.torrent-health');
        
        indicator.className = `torrent-health ${healthStatus}`;
        
        // Actualizar tooltips
        const tooltip = {
            'healthy': 'Torrent saludable',
            'medium': 'Velocidad media',
            'poor': 'Pocos seeds'
        };
        
        indicator.setAttribute('title', tooltip[healthStatus]);
    }

    calculateHealth(seeds, peers) {
        if (seeds > 10) return 'healthy';
        if (seeds > 5) return 'medium';
        return 'poor';
    }

    startPeriodicUpdate(containers) {
        setInterval(() => {
            containers.forEach(container => {
                const infoHash = container.dataset.torrentHash;
                this.updateStats(infoHash).then(stats => {
                    if (stats) this.updateTorrentDisplay(container, stats);
                });
            });
        }, 300000); // Actualizar cada 5 minutos
    }
}