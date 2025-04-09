class TorrentTracker {
    constructor() {
        this.updateInterval = 30000; // 30 segundos
    }

    async updateStats(infoHash) {
        // Simulación de stats - En producción esto se conectaría a un tracker real
        return {
            seeds: Math.floor(Math.random() * 200) + 1,
            peers: Math.floor(Math.random() * 100) + 1
        };
    }

    updateTorrentDisplay(container, stats) {
        const seedsElement = container.querySelector('.seeds-indicator + span');
        const peersElement = container.querySelector('.peers-indicator + span');
        
        if (seedsElement) seedsElement.textContent = `Seeds: ${stats.seeds}`;
        if (peersElement) peersElement.textContent = `Peers: ${stats.peers}`;
    }

    startPeriodicUpdate(containers) {
        setInterval(() => {
            containers.forEach(container => {
                const infoHash = container.dataset.torrentHash;
                this.updateStats(infoHash).then(stats => {
                    if (stats) this.updateTorrentDisplay(container, stats);
                });
            });
        }, this.updateInterval);
    }
}