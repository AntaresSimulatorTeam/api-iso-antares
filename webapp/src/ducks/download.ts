import { Action, AnyAction } from 'redux';
import { ThunkAction } from 'redux-thunk';
import { v4 as uuidv4 } from 'uuid';
import { AppState } from '../App/reducers';
import { addOnCloseListener, removeOnCloseListener } from './global';


/** ******************************************* */
/* State                                        */
/** ******************************************* */

export interface UploadItem {
  id: string;
  name: string;
  completion: number;
}

export interface DownloadItem {
  name: string;
  url: string;
}

export interface DownloadState {
  downloads: DownloadItem[];
  onWindowCloseListenerId?: string;
}

const initialState: DownloadState = {
  downloads: [],
};

/** ******************************************* */
/* Actions                                      */
/** ******************************************* */

export interface UploadGlobalListenerAction extends Action {
  type: 'DOWNLOAD/UPDATE_GLOBAL_LISTENER';
  payload?: string;
}

export interface AddDownloadAction extends Action {
  type: 'DOWNLOAD/ADD';
  payload: DownloadItem;
}

export const addDownload = (downloadItem: DownloadItem): ThunkAction<string, AppState, unknown, AnyAction> => (dispatch): string => {
  const uploadId = uuidv4();
  // const listenerId = dispatch(addOnCloseListener(() => 'Refreshing will abort current download operation'));
  // dispatch({
  //   type: 'DOWNLOAD/UPDATE_GLOBAL_LISTENER',
  //   payload: listenerId,
  // });
  dispatch({
    type: 'DOWNLOAD/ADD',
    payload: downloadItem,
  });
  return uploadId;
};


export interface ClearDownloadAction extends Action {
  type: 'DOWNLOAD/CLEAR';
  payload: string;
}

export const clearDownload = (id: string): ThunkAction<void, AppState, unknown, AnyAction> => (dispatch, getState): void => {
  const { upload } = getState();
  if (upload.uploads.length === 1 && !!upload.uploads.find((el) => el.id === id) && upload.onWindowCloseListenerId) {
    dispatch(removeOnCloseListener(upload.onWindowCloseListenerId));
  }
  dispatch({
    type: 'DOWNLOAD/CLEAR',
    payload: id,
  });
};


type DownloadAction = AddDownloadAction | ClearDownloadAction | UploadGlobalListenerAction;

/** ******************************************* */
/* Selectors / Misc                             */
/** ******************************************* */


/** ******************************************* */
/* Reducer                                      */
/** ******************************************* */

export default (state = initialState, action: DownloadAction): DownloadState => {
  switch (action.type) {
    case 'DOWNLOAD/ADD':
      return {
        ...state,
        downloads: state.downloads.concat(action.payload),
      };
    case 'DOWNLOAD/CLEAR': {
      const newState: DownloadState = {
        ...state,
        downloads: state.downloads.filter((u) => u.url !== action.payload),
      };
      return newState;
    }
    case 'DOWNLOAD/UPDATE_GLOBAL_LISTENER': {
      const newState: DownloadState = { ...state };
      if (action.payload) {
        newState.onWindowCloseListenerId = action.payload;
      } else {
        delete newState.onWindowCloseListenerId;
      }
      return newState;
    }
    default:
      return state;
  }
};
