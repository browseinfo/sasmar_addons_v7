openerp.account.quickadd = function (instance) {
    var _t = instance.web._t,
        _lt = instance.web._lt;
    var QWeb = instance.web.qweb;
    
    instance.web.account = instance.web.account || {};

    instance.web.views.add('tree_account_move_line_quickadd', 'instance.web.account.QuickAddListView');
    instance.web.account.QuickAddListView = instance.web.ListView.extend({
        init: function() {
            this._super.apply(this, arguments);
            this.journals = [];
            this.periods = [];
            this.company = [];
            this.current_journal = null;
            this.current_period = null;
            this.current_company = null;
            this.default_period = null;
            this.default_journal = null;
            this.default_company = null;
            this.current_journal_type = null;
            this.current_journal_currency = null;
            this.current_journal_analytic = null;
        },
        start:function(){
            var tmp = this._super.apply(this, arguments);
            var self = this;
            this.$el.parent().prepend(QWeb.render("AccountMoveLineQuickAdd", {widget: this}));
            
            this.$el.parent().find('.oe_account_select_journal').change(function() {
                    self.current_journal = this.value === '' ? null : parseInt(this.value);
					console.log("self",self);
                    self.do_search(self.last_domain, self.last_context, self.last_group_by);
                });
            this.$el.parent().find('.oe_account_select_period').change(function() {
                    self.current_period = this.value === '' ? null : parseInt(this.value);
					console.log("self",self);
                    self.do_search(self.last_domain, self.last_context, self.last_group_by);
                });
                
            this.$el.parent().find('.oe_account_select_company').change(function() {
                    self.current_company = this.value === '' ? null : parseInt(this.value);
					var mod = new instance.web.Model("account.move.line", self.last_context, self.last_domain);
					mod.call("get_periods_per_company", [this.value]).then(function(result) {
						console.log("result of method",result);   
						self.periods = result;
				        self.$el.parent().find('.oe_account_select_period').children().remove().end();
				        self.$el.parent().find('.oe_account_select_period').append(new Option('', ''));
				        for (var i = 0;i < self.periods.length;i++){
				            o = new Option(self.periods[i][1], self.periods[i][0]);
				            self.$el.parent().find('.oe_account_select_period').append(o);
				        }    
				        self.$el.parent().find('.oe_account_select_period').val(self.current_period).attr('selected',true);
					});
					mod.call("get_journals_per_company", [this.value]).then(function(result) {
						self.journals = result;
				        var o;
				        self.$el.parent().find('.oe_account_select_journal').children().remove().end();
				        self.$el.parent().find('.oe_account_select_journal').append(new Option('', ''));
				        for (var i = 0;i < self.journals.length;i++){
				            o = new Option(self.journals[i][1], self.journals[i][0]);
				            if (self.journals[i][0] === self.current_journal){
				                self.current_journal_type = self.journals[i][2];
				                self.current_journal_currency = self.journals[i][3];
				                self.current_journal_analytic = self.journals[i][4];
				                $(o).attr('selected',true);
				            }
						}
				            self.$el.parent().find('.oe_account_select_journal').append(o);										
					});
				            //self.do_search(self.last_domain, self.last_context, self.last_group_by);
			});

            this.on('edit:after', this, function () {
                self.$el.parent().find('.oe_account_select_journal').attr('disabled', 'disabled');
                self.$el.parent().find('.oe_account_select_period').attr('disabled', 'disabled');
                self.$el.parent().find('.oe_account_select_company').attr('disabled', 'disabled');
            });
            this.on('save:after cancel:after', this, function () {
                self.$el.parent().find('.oe_account_select_journal').removeAttr('disabled');
                self.$el.parent().find('.oe_account_select_period').removeAttr('disabled');
                self.$el.parent().find('.oe_account_select_company').removeAttr('disabled');
            });

            var mod = new instance.web.Model("account.move.line", self.dataset.context, self.dataset.domain);
            mod.call("default_get", [['journal_id','period_id','company_id'],self.dataset.context]).then(function(result) {
                self.current_period = result['period_id'];
                self.current_journal = result['journal_id'];
                self.current_company = result['company_id'];
            });
            return tmp;
        },
        do_search: function(domain, context, group_by) {
			console.log("domain",domain);
			console.log("context",context);
            var self = this;
            this.last_domain = domain;
            this.last_context = context;
            this.last_group_by = group_by;
            this.old_search = _.bind(this._super, this);
            var mod = new instance.web.Model("account.move.line", context, domain);
            console.log('############', mod);
            return $.when(mod.call("list_journals", []).then(function(result) {
                self.journals = result;
            }),mod.call("list_periods", []).then(function(result) {
                self.periods = result;
            }),mod.call("list_company", []).then(function(result) {
                self.company = result;
                console.log('resultcompany============',self.company);
            })).then(function () {
                var o;
                self.$el.parent().find('.oe_account_select_journal').children().remove().end();
                self.$el.parent().find('.oe_account_select_journal').append(new Option('', ''));
                for (var i = 0;i < self.journals.length;i++){
                    o = new Option(self.journals[i][1], self.journals[i][0]);
                    if (self.journals[i][0] === self.current_journal){
                        self.current_journal_type = self.journals[i][2];
                        self.current_journal_currency = self.journals[i][3];
                        self.current_journal_analytic = self.journals[i][4];
                        $(o).attr('selected',true);
                    }
                    self.$el.parent().find('.oe_account_select_journal').append(o);
                }
                self.$el.parent().find('.oe_account_select_period').children().remove().end();
                self.$el.parent().find('.oe_account_select_period').append(new Option('', ''));
                for (var i = 0;i < self.periods.length;i++){
                    o = new Option(self.periods[i][1], self.periods[i][0]);
                    self.$el.parent().find('.oe_account_select_period').append(o);
                }    
                self.$el.parent().find('.oe_account_select_period').val(self.current_period).attr('selected',true);

                self.$el.parent().find('.oe_account_select_company').children().remove().end();
                self.$el.parent().find('.oe_account_select_company').append(new Option('', ''));
                for (var i = 0;i < self.company.length;i++){
                	console.log('nxxxxxxxxxxxxxxxxxxxxxxxx',self.company[i]);
                    o = new Option(self.company[i][1], self.company[i][0]);
                    self.$el.parent().find('.oe_account_select_company').append(o);
                }    
                self.$el.parent().find('.oe_account_select_company').val(self.current_company).attr('selected',true);

                return self.search_by_journal_period();
 
            });
        },
        search_by_journal_period: function() {
            var self = this;
            var domain = ['|',['debit', '!=', 0], ['credit', '!=', 0]];
            if (self.current_journal !== null) domain.push(["journal_id", "=", self.current_journal]);
            if (self.current_period !== null) domain.push(["period_id", "=", self.current_period]);
            if (self.current_company !== null) domain.push(["company_id", "=", self.current_company]);

            self.last_context["journal_id"] = self.current_journal === null ? false : self.current_journal;
            if (self.current_period === null) delete self.last_context["period_id"];
            else self.last_context["period_id"] =  self.current_period;

            if (self.current_company === null) delete self.last_context["company_id"];
            else self.last_context["company_id"] =  self.current_company;

            self.last_context["journal_type"] = self.current_journal_type;
            self.last_context["currency"] = self.current_journal_currency;
            self.last_context["analytic_journal_id"] = self.current_journal_analytic;
            return self.old_search(new instance.web.CompoundDomain(self.last_domain, domain), self.last_context, self.last_group_by);
        },
    });
};
