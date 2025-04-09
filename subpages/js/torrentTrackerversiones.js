class TorrentTracker {
    constructor() {
        this.updateInterval = 30000; // 30 segundos
    }

    async updateStats(infoHash) {
        try {
            // Simulación de estadísticas de torrent
            // En un caso real, aquí se conectaría con un tracker real
            return {
                seeds: Math.floor(Math.random() * 200) + 1,  // Random entre 1-200
                peers: Math.floor(Math.random() * 100) + 1   // Random entre 1-100
            };
        } catch (error) {
            console.error('Error updating torrent stats:', error);
            return null;
        }
    }

    updateTorrentDisplay(container, stats) {
        const seedsSpan = container.querySelector('.seeds-indicator + span');
        const peersSpan = container.querySelector('.peers-indicator + span');

        if (seedsSpan) {
            seedsSpan.textContent = `Seeds: ${stats.seeds}`;
            const indicator = container.querySelector('.seeds-indicator');
            if (indicator) {
                indicator.className = 'seeds-indicator ' + 
                    (stats.seeds > 0 ? 'active' : 'inactive');
            }
        }

        if (peersSpan) {
            peersSpan.textContent = `Peers: ${stats.peers}`;
            const indicator = container.querySelector('.peers-indicator');
            if (indicator) {
                indicator.className = 'peers-indicator ' + 
                    (stats.peers > 0 ? 'active' : 'inactive');
            }
        }
    }

    startPeriodicUpdate(containers) {
        // Actualización inicial
        containers.forEach(container => {
            const infoHash = container.dataset.torrentHash;
            this.updateStats(infoHash).then(stats => {
                if (stats) this.updateTorrentDisplay(container, stats);
            });
        });

        // Actualización periódica
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