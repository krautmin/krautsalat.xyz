function multiselectComponent() {
    return {
        listActive: false,
        selectedString: '',
        selected: [],
        unselected: ["volvo", "saab", "opel", "audi", "mercedes", "mazda"],
        addMe(e) {
            const index = e.target.dataset.index;
            const extracted = this.unselected.splice(index, 1);
            this.selected.push(extracted[0]);
        },
        removeMe(e) {
            const index = e.target.dataset.index;
            const extracted = this.selected.splice(index, 1);
            this.unselected.push(extracted[0]);
        }
    };
}