openerp.web_doc = function (instance) {
    var QWeb = instance.web.qweb;
          _t = instance.web._t;
          view_info = new instance.web.ViewManager;
    instance.web.DocButton = instance.web.Widget.extend({
        template:'web_doc.DocButton',
    });

    instance.web.DocButton.include({
        
        init: function (parent) {
            this.av = parent;
            this._super(parent);
        },
        
        start: function () {
            this.$('a.oe_doc_doc_show').on('click', this.on_see_doc );
            this.$('.oe_doc_doc_hide').on('click', this.on_hide_doc );
            this.$('a.oe_edit_help').on('click', this.on_edit_help );
            this.$('a.oe_set_help').on('click', this.on_set_help );
            this.$('a.oe_create_help').on('click', this.on_create_help );
            this._super();
        },

        on_set_help: function() {
            var self = this;                                                            
                self.rpc("/web/action/load", 
                    { action_id: "web_doc.set_help_action" })
                    .done(function(result) {
                    self.getParent().do_action( result, {
                        additional_context: {
                            'search_default_id': result.doc_id,
                            'active_id': result.doc_id,
                            'action_doc_enviroment': self.av.action.id,
                        },
                    });
                    $(".openerp .oe_doc_float_help").fadeOut( 200, function(){
                    });
                });                                                             
        },  

        on_edit_help: function() {
            var self = this;                                                            
                self.rpc("/web/action/load", 
                    { action_id: "vauxoo_cms.cms_action_tree" })
                    .done(function(result) {
                    self.getParent().do_action( result, {
                        additional_context: {
                            'search_default_id': result.doc_id,
                            'active_id': result.doc_id,
                            'action_doc_enviroment': self.av.action.id
                        },
                    });
                    $(".openerp .oe_doc_float_help").fadeOut( 200, function(){
                    });
                });                                                             
        },  

        on_create_help: function() {
            var self = this;                                                            
                self.rpc("/web/action/load", { 
                         action_id: "web_doc.document_action_form" 
                         }).done(function(result) {
                    self.getParent().do_action(result, {
                        additional_context: {
                            'default_name': self.av.action.name,
                            'default_content': self.av.action.help,
                            'action_doc_enviroment': self.av.action.id,
                        },
                    });                  
                    var v = new instance.web.View;
                    v.reload();
                    $(".openerp .oe_doc_float_help").fadeOut( 200, function(){
                    });
                });                                                                 
        },  

        on_see_doc: function() {
            $(".openerp .oe_doc_float_help").fadeIn(400);
        },

        on_hide_doc: function() {
            $(".openerp .oe_doc_float_help").fadeOut( 200);
        },
        
        renderElement: function() {
            this._super();
        },

        destroy: function () {            
            this._super();
        }
    });

    instance.web.ViewManager.include({

        start: function () {
            var self = this;
            if (! this.isEmpty(this.action)) {
                var doc_button = new instance.web.DocButton(self);
                if ($('.oe_topbar_doc_doc').length == 0){
                    doc_button.appendTo(instance.webclient.$el.find('.oe_systray'));
                };
                instance.doc_button = doc_button;
            };
            if (! this.isEmpty(doc_button)) {
                doc_button.$el.find('a.oe_link-process').on('click' , function(ev) { 
                    self.initialize_process_view(ev);
                    $(".openerp .oe_doc_float_help").fadeOut(200);
                });
            };
            return self._super();
        },

        isEmpty: function (obj) {
            if (typeof obj == 'undefined' || obj === null || obj === '') return true;
            if (typeof obj == 'number' && isNaN(obj)) return true;
            if (obj instanceof Date && isNaN(Number(obj))) return true;
            return false;
        },
        
    });
};
