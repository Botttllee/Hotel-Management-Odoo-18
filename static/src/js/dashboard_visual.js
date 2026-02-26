/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

const { Component, onWillStart, onWillUnmount, useState } = owl;

class HotelDashboardVisual extends Component {
    setup() {
        this.orm = useService("orm");
        this.state = useState({
            loading: true,
            metrics: {},
            error: false,
        });

        onWillStart(async () => {
            await this._loadMetrics();
        });

        this.refreshTimer = setInterval(() => this._loadMetrics(), 30000);
        onWillUnmount(() => {
            clearInterval(this.refreshTimer);
        });
    }

    async _loadMetrics() {
        try {
            const result = await this.orm.call("hotel.dashboard", "get_dashboard_metrics", []);
            this.state.metrics = result || {};
            this.state.error = false;
        } catch (error) {
            this.state.error = true;
        } finally {
            this.state.loading = false;
        }
    }

    get occupancyWidth() {
        const value = Number(this.state.metrics.occupancy_rate || 0);
        return `${Math.max(0, Math.min(100, value)).toFixed(2)}%`;
    }
}

HotelDashboardVisual.template = "hotelv18.DashboardVisual";

registry.category("actions").add("hotelv18.dashboard_visual_action", HotelDashboardVisual);
