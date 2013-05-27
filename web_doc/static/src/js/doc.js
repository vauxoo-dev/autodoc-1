openerp.web_doc = function (instance) {
    var QWeb = instance.web.qweb;
          _t = instance.web._t;
          view_info = instance.web.ViewManager;
    instance.web.DocButton = instance.web.Widget.extend({
        template:'web_doc.DocButton',
    });

    instance.web.DocButton.include({
        
        init: function (parent) {
            this.av = parent;
            view_info = this.av;
            this._super(parent);
        },
        
        start: function () {
            this.$('a.oe_doc_doc_show').on('click', this.on_see_doc );
            this.$('.oe_doc_doc_hide').on('click', this.on_hide_doc );
            this.$('a.oe_edit_help').on('click', this.on_edit_help );
            this.$('a.oe_create_help').on('click', this.on_create_help );
            this.$el.find('a.oe_link-process').on('click' , function(ev) { 
                view_info.initialize_process_view(ev);
                $(".openerp .oe_doc_float_help").fadeOut( 200, function(){
                });
            });
            this._super();
        },

        on_edit_help: function() {
            var self = this;                                                            
                self.rpc("/web/action/load", { action_id: "vauxoo_cms.cms_action_tree" }).done(function(result) {
                    result.view_type = 'form';
                    console.log(result);
                    self.getParent().do_action( result, {
                        additional_context: {
                            'search_default_id': result.doc_id,
                            'active_id': result.doc_id,
                            'view_type': 'form',
                        },
                    });
                    var v = new instance.web.View;
                    v.reload();
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
            this.rpc("/doc/generic/doc_info", {}).done(function(res) {
                $(".openerp .oe_doc_float_help").fadeIn(400);
            });
        },

        on_hide_doc: function() {
            this.rpc("/doc/generic/doc_info", {}).done(function(res) {
                $(".openerp .oe_doc_float_help").fadeOut( 200, function(){
                });
            });
        },
        
        renderElement: function() {
            this._super();
        },

        destroy: function () {            
            var self=this;
            this._super();
        }

    });

    instance.web.ViewManager.include({

        start: function () {
            this._super.apply(this, arguments);
            var self = this;
            if (! this.isEmpty(this.action)) {
                var doc_button = new instance.web.DocButton(self);
                doc_button.appendTo(instance.webclient.$el.find('.oe_systray'));
                instance.doc_button = doc_button;
            }
        },
        
        isEmpty: function (obj) {
            if (typeof obj == 'undefined' || obj === null || obj === '') return true;
            if (typeof obj == 'number' && isNaN(obj)) return true;
            if (obj instanceof Date && isNaN(Number(obj))) return true;
            return false;
        },
        
        inspect: function (obj) {
          var msg = '';

          for (var property in obj)
          {
            if (typeof obj[property] == 'function')
            {
              var inicio = obj[property].toString().indexOf('function');
              var fin = obj[property].toString().indexOf(')')+1;
              var propertyValue=obj[property].toString().substring(inicio,fin);
              msg +=(typeof obj[property])+' '+property+' : '+propertyValue+' ;\n';
            }
            else if (typeof obj[property] == 'unknown')
            {
              msg += 'unknown '+property+' : unknown ;\n';
            }
            else
            {
              msg +=(typeof obj[property])+' '+property+' : '+obj[property]+' ;\n';
            }
          }
          return msg;
        },
        
        process_edit_view: function() {
            var self = this;
            var pop = new instance.web.form.FormOpenPopup(self);
            pop.show_element(
                self.process_dataset.model,
                self.process_id,
                self.context || self.dataset.context,
                {
                    title: _t('Process')
                });
            var form_controller = pop.view_form;
            pop.on('write_completed', self, self.initialize_process_view);
        },
    });
 };
