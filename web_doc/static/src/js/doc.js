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
        
        cut_doc: function(event){
            var slideHeight = 75; // px
            var defHeight = event[0];
            if(defHeight >= slideHeight){
                $('#wrap').css('height' , slideHeight + 'px');
                $('#read-more').append('<a href="#">Click to Read More</a>');
                $('#read-more a').click(function(){
                    var curHeight = $('#wrap').height();
                    if(curHeight == slideHeight){
                        $('#wrap').animate({
                          height: defHeight
                        }, "normal");
                        $('#read-more a').html('Close');
                        $('#gradient').fadeOut();
                    }else{
                        $('#wrap').animate({
                          height: slideHeight
                        }, "normal");
                        $('#read-more a').html('Click to Read More');
                        $('#gradient').fadeIn();
                    }
                    return false;
                });
            }
        },

        on_edit_help: function() {
            var self = this;                                                            
                self.rpc("/web/action/load", { action_id: "vauxoo_cms.cms_action_tree" }).done(function(result) {
                    self.getParent().do_action(result, {
                        additional_context: {
                            // SEARCH DEFAULT IS NOT WORKING,
                            // TODO: 'search_default_name': ['Category'],
                        },
                    });                  
                });                                                                     
        },  

        on_create_help: function() {
            var self = this;                                                            
                self.rpc("/web/action/load", { 
                         action_id: "web_doc.document_action_form" 
                         }).done(function(result) {
                    self.getParent().do_action(result, {
                        action_menu_id: 143,
                        additional_context: {
                            'default_name': result.name,
                        },
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
        /**
         * Opens a given menu by id, as if a user had browsed to that menu by hand
         * except does not trigger any event on the way
         * The only difference is that we change the parameters to be sure the button
         * On menu has the correct context, to open the process.
         *
         * @param {Number} id database id of the terminal menu to select
         */
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
