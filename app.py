import streamlit as st
import pandas as pd
from dataclasses import dataclass
from datetime import datetime
from database import Database

DATABASE_PATH = "annotation.db"
db = Database(DATABASE_PATH)

tbdfs = [
    '', 'None', 'Bitter frustration', 'Impatience', 'Irony', 'Insulting', 'Mocking', 'Threat', 'Vulgarity',
    'Entitlement', 'Identity attacks/Name-Calling', 'Other'
]
triggers = [
    '', 'None', 'Failed use of tool/code or error messages', 'Communication breakdown', 'Rejection',
    'Violation of community conventions', 'Past interactions', 'Politics/ideology', 'Technical disagreement',
    'Unprovoked', 'Other'
]
targets = [
    '', 'None', 'Code/tool', 'People', 'Company/organization', 'Self-directed', 'Undirected', 'Other'
]
consequences = [
    '', 'None', 'Invoke Code of Conduct', 'Escalating further', 'Discontinued further discussion',
    'Provided technical explanation', 'Accepting criticism', 'Trying to stop the incivility', 'Other'
]


@dataclass
class AnnotatedComment:
    """
    Dataclass to store a comment with an id and an annotation
    """
    comment_id: int
    issue_id: int
    user_id: int
    created_at: str
    comment_body: str
    annotation = "None"
    annotation_other = ""


df_comments = pd.read_csv('comments_v2.csv')
df_issues = pd.read_csv('merged_threads_v2_1.csv')


def next():
    st.session_state.counter += 1
    st.session_state.issue_level = 1


def insert_comment(issue_id, comment_id, user_login, tbdf):
    st.session_state.counter += 1
    st.session_state.issue_level = 1
    db.insert_comment_annotation(issue_id, comment_id, user_login, tbdf)


def next_issue(next_issue_id, user_login, issue_id, derailment_point, trigger, target, consequences,
               additional_comments):
    st.session_state.counter += 1
    st.session_state.issue_level = 1
    st.session_state.comments_on_screen = []
    db.update_current_issue(user_login, next_issue_id)
    db.insert_issue_annotation(issue_id, user_login, derailment_point, trigger, target, consequences,
                               additional_comments)
    js = '''
                    <script>
                        var body = window.parent.document.querySelector(".main");
                        console.log(body);
                        body.scrollTop = 0;
                    </script>
                    '''

    st.components.v1.html(js)


def finish_annotation():
    st.session_state.annotation_finished = 1


def next_issue_level():
    # st.session_state.counter += 1
    st.session_state.issue_level = 0


def prev():
    if st.session_state.counter != 0:
        st.session_state.counter -= 1


def st_on_change(comment, option):
    comment.annotation = option


if 'counter' not in st.session_state: st.session_state.counter = 0

if 'annotation_finished' not in st.session_state: st.session_state.annotation_finished = 0

if 'logged_in' not in st.session_state: st.session_state.logged_in = 0

if 'user_login' not in st.session_state: st.session_state.user_login = ''

if 'issue_level' not in st.session_state: st.session_state.issue_level = 1

if "issue_id" not in st.session_state:
    st.session_state.issue_id = 0

if "comments_on_screen" not in st.session_state:
    comments_on_screen = []
    st.session_state.comments_on_screen = comments_on_screen
else:
    comments_on_screen = st.session_state.comments_on_screen

# Load comment and the current annotations
if "my_comments" not in st.session_state:
    comments = df_comments.to_dict(orient='records')
    my_comments = [AnnotatedComment(comment_id=comments[i].get('comment_id'),
                                    issue_id=comments[i].get('issue_id'),
                                    comment_body=comments[i].get('comment_body'),
                                    user_id=comments[i].get('user_id'),
                                    created_at=comments[i].get('created_at')
                                    ) for i in range(len(comments))]
    st.session_state.my_comments = my_comments
else:
    my_comments = st.session_state.my_comments


def inject_css():
    s = f"""
        <style>
        blockquote {{background-color: #dfdfe1; border-radius: 5px}}
        <style>
        """
    st.markdown(s, unsafe_allow_html=True)


def instructions():
    return '''
    # [Link to Instructions](https://docs.google.com/document/d/1AjVhj_Jgg6nxLh-1oD6r1nVMdxCQCX98aWfYu89IT3E/edit?usp=sharing)
    ## Table 1 - Uncivil Features
    **Bitter frustration**: when someone expresses strong frustration
    
    **Impatience**: participants might demonstrate impatience when they express a feeling that it is taking too long to solve a problem, understand a solution, or answer a question
    
    **Irony**: contributors used expressions that usually signify the opposite in a mocking or blaming tone
    
    **Insulting**: Insulting remarks directed at another person
    
    **Mocking**: when a discussion participant is making fun of someone else, usually because that person has made a mistake
    
    **Threat**: contributors put a condition impacting the result of another discussion participant or that person’s career
    
    **Vulgarity**: using profanity or language that is not considered proper
    
    **Entitlement**: expecting special privileges, attention, or resources without regard for the norms of collaboration and respect
    
    **Identity attack/Name-Calling**: Race, Religion, Nationality, Gender, Sexual-oriented, or any other kind of attacks and mean/offensive words directed at someone or a gorup of people
    
    ## Table 2 - Triggers
    **Failed use of tool/code or error messages**: trouble with code/tool
    
    **Communication breakdown**: being misinterpreted by people or being unable to follow
    
    **Rejection**: receiving a quick rejection or a rejection without sufficient explanation
    
    **Violation of community conventions**: disagreement with the workflow imposed by the community
    
    **Past interactions**: comments are posted that refer to past interactions of the author with the project
    
    **Politics/ideology**: arising over politics or ideology differences (specific beliefs)
    
    **Technical disagreement**: have differing views on some technical component of the project
    
    **Unprovoked**: uncivil behavior or hostility occurs without an apparent reason or trigger
    
    ## Table 3 - Targets
    **Code/tool**: code (things or objects)
    
    **People**: targeted at people
    
    **Company/organization**: targeted at companies or organizations
    
    **Self-directed**: targeted at self
    
    **Undirected**: can’t be targeted at people/things. Mostly in the form of profanities
    
    ## Table 4 - Consequences
    **Invoke Code of Conduct**: moderators/maintainers invoking CoC
    
    **Turning constructive**: after the uncivil comment, discussion becomes constructive (no more uncivil comments)
    
    **Escalating further**: more uncivil messages are exchanged after the first one
    
    **Discontinued further discussion**: no more messages are exchanged
    
    **Provided technical explanation**: provide technical explanations even after receiving uncivil comment
    
    **Accepting criticism**: they accept the criticisms instead of closing/locking the issue, or discontinuing further discussion
    
    **Trying to stop the incivility**: actively trying to put a stop to incivility, but not necessarily invoking Code of Conduct
    '''


def main():
    inject_css()
    print(st.session_state.logged_in)
    logged_in = st.session_state.logged_in
    user_login = ''
    if not logged_in:
        with st.form("my_form"):
            st.write("Please login with the provided login info")
            user_login = st.text_input('User Login')
            submitted = st.form_submit_button("Submit")
            if submitted:
                user = db.get_user(user_login)
                if user is None:
                    st.toast('User not found!')
                else:
                    st.session_state.logged_in = 1
                    st.session_state.user_login = user_login
                    if st.session_state.user_login != 'admin':
                        current_issue_id = user.get('current_issue_id')
                        end_issue_id = user.get('end_issue_id')
                        if current_issue_id == end_issue_id:
                            st.session_state.annotation_finished = 1
                        logged_in = 1
                        st.rerun()
                    else:
                        logged_in = 1
                        st.rerun()
    elif st.session_state.user_login == 'admin':
        with open("annotation.db", "rb") as fp:
            btn = st.download_button(
                label="Download db file",
                data=fp,
                file_name="annotation.db",
                mime="application/octet-stream"
            )
    else:
        if st.session_state.annotation_finished:
            st.empty()
            st.markdown('# Annotations Completed! Thanks for your participation!')
            st.balloons()
        else:
            user = db.get_user(st.session_state.user_login)
            current_issue_id = user.get('current_issue_id')
            print(current_issue_id)
            st.session_state.issue_id = current_issue_id
            while True:
                comment = my_comments[st.session_state.counter % (len(my_comments))]
                if comment.issue_id != current_issue_id:
                    next()
                else:
                    break
            next_comment = my_comments[(st.session_state.counter + 1) % (len(my_comments))]

            issues = df_issues.to_dict(orient='records')
            issue_titles = {}
            for issue in issues:
                issue_titles[issue.get('issue_id')] = issue.get('issue_title')

            # if comment.issue_id != st.session_state.issue_id:
            #     st.session_state.comments_on_screen = []

            # st.session_state.issue_id = comment.issue_id

            # if next_comment.issue_id != st.session_state.issue_id:
            #     if len(st.session_state.comments_on_screen) != 0:
            #         st.info('Please indicate the derailment point, trigger, target, and consequences')

            st.write("""
                     # Issue {}
                     ## {}
                     """.format(st.session_state.issue_id, issue_titles[st.session_state.issue_id]))
            cols = st.columns([3, 1])

            # with cols[0]:
            n = 0
            if comment not in st.session_state.comments_on_screen:
                st.session_state.comments_on_screen.append(comment)
            print(len(st.session_state.comments_on_screen))

            with st.sidebar:
                progress_text = "Comments remaining in this issue"
                all_comments_to_display = []
                for comment in my_comments:
                    if comment.issue_id == st.session_state.issue_id:
                        all_comments_to_display.append(comment)
                my_bar = st.progress(0, text=progress_text)
                percent = (len(st.session_state.comments_on_screen)) / len(all_comments_to_display)
                if percent == 1:
                    progress_text = "Comments completed!"
                my_bar.progress((len(st.session_state.comments_on_screen)) / len(all_comments_to_display), progress_text)
                st.write(instructions())

            for comment in st.session_state.comments_on_screen:
                with st.chat_message("user"):
                    datetime_object = datetime.strptime(comment.created_at, '%Y-%m-%dT%H:%M:%SZ')
                    metadata = """
                                ##### User {}
                                {},     **Comment {}**
                            """.format(comment.user_id, datetime_object, str(n))
                    st.write(metadata)
                    comment_body = comment.comment_body
                    comment_body = comment_body.replace("```", '').replace("##", '')
                    st.write(comment_body)
                    st.markdown('---')
                    option = st.selectbox(label='Select TBDF', options=tbdfs, key=comment.comment_id, index=0)
                    comment.annotation = option

                    if n > 0:
                        st.markdown('---')
                        option = st.selectbox(label='Is the comment Toxic?', options=["","Yes", "No"], key=(comment.comment_id*2), index=0)

                    n += 1
                # if comment.annotation == 'Other':
                #     comment.annotation_other = st.text_input('Enter TBDF')

            if next_comment.issue_id != st.session_state.issue_id:
                if st.session_state.issue_level == 1:
                    st.button("Issue level ➡️", on_click=next_issue_level, use_container_width=True)
                primary_color = st.get_option("theme.primaryColor")
                s = f"""
                <style>
                div.stButton > button:first-child {{ border: 5px solid {primary_color}; background-color: #FF4081; color: white;}}
                blockquote {{background-color: #dfdfe1; border-radius: 5px}}
                <style>
                """
                st.markdown(s, unsafe_allow_html=True)
            else:
                comment_id = comment.comment_id
                comment_annotation = comment.annotation
                print('comment_id:' + str(comment_id))
                st.button("Next Comment ⬇️", on_click=insert_comment, use_container_width=True, args=(current_issue_id,
                                                                                                      comment_id,
                                                                                                      st.session_state.user_login,
                                                                                                      comment_annotation))
            if not st.session_state.issue_level:
                st.info('Please indicate the derailment point, trigger, target, and consequences')
                dps = ['']
                for i in range(len(st.session_state.comments_on_screen)):
                    c = st.session_state.comments_on_screen[i]
                    dps.append("Comment {}, {}".format(i, c.annotation))
                option_derail = st.selectbox(
                    'Derailment Point',
                    dps,
                    disabled=st.session_state.issue_level,
                    key='derailment point' + str(st.session_state.issue_id))
                option_trigger = st.selectbox(
                    'Trigger',
                    triggers,
                    disabled=st.session_state.issue_level,
                    key='option_trigger' + str(st.session_state.issue_id))
                option_target = st.selectbox(
                    'Target',
                    targets,
                    disabled=st.session_state.issue_level,
                    key='option_target' + str(st.session_state.issue_id))
                option_consequences = st.multiselect(
                    'Consequences',
                    consequences,
                    disabled=st.session_state.issue_level,
                    key='option_consequences' + str(st.session_state.issue_id))
                additional_comments = st.text_input('Additional Comments', key='additional_comments' + str(st.session_state.issue_id))
                if st.session_state.issue_level == 0:
                    current_issue_id = user.get('current_issue_id')
                    end_issue_id = user.get('end_issue_id')
                    if current_issue_id != end_issue_id:
                        st.button("Next Issue ✅", on_click=next_issue, use_container_width=True,
                                  args=(next_comment.issue_id, st.session_state.user_login, comment.issue_id, option_derail,
                                        option_trigger, str(option_target), str(option_consequences), additional_comments))
                    else:
                        st.button("Finish Annotation ✅", on_click=finish_annotation, use_container_width=True)
        # with cols[1]:
        #     dps = []
        #     for i in range(len(st.session_state.comments_on_screen)):
        #         c = st.session_state.comments_on_screen[i]
        #         dps.append("Comment {}, {}".format(i, c.annotation))
        #     option_derail = st.selectbox(
        #         'Derailment Point',
        #         dps,
        #         disabled=st.session_state.issue_level,
        #         key='derailment point')
        #     option_trigger = st.selectbox(
        #         'Trigger',
        #         triggers,
        #         disabled=st.session_state.issue_level,
        #         key='option_trigger')
        #     option_target = st.selectbox(
        #         'Target',
        #         targets,
        #         disabled=st.session_state.issue_level,
        #         key='option_target')
        #     option_consequences = st.multiselect(
        #         'Consequences',
        #         consequences,
        #         disabled=st.session_state.issue_level,
        #         key='option_consequences')
        #     if st.session_state.issue_level == 0:
        #         st.button("Next Issue ✅", on_click=next_issue, use_container_width=True,
        #                   args=(st.session_state.user_login, next_comment.issue_id, option_derail,
        #                         option_trigger, str(option_target), str(option_consequences)))

    # Using "with" notation

    # with cols[0]:
    #     st.button("⬅️ Previous", on_click=prev, use_container_width=True)


if __name__ == "__main__":
    main()
